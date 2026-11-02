#!/usr/bin/env python3
"""Regenerate the site's content files from scripts/benabdeslem-site-data.json.

Writes:
  _publications/*.html one file per publication (the folder is emptied first)
  _data/*.yml          profile, students, projects, teaching, cv, resources, contact, archive_2010

Usage (from the repository root):
  pip install pyyaml
  python3 scripts/json_to_site.py

Hand-written pages live in _pages/ and are never touched by this script.
"""
import datetime
import json
import pathlib
import re
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "benabdeslem-site-data.json"
PUB_DIR = ROOT / "_publications"
DATA_DIR = ROOT / "_data"

CATEGORY = {"journal": "journals", "conference": "conferences", "patent": "patents",
            "editorial": "editorial", "thesis": "theses"}


class Dumper(yaml.SafeDumper):
    pass


def _str_presenter(dumper, value):
    return dumper.represent_scalar("tag:yaml.org,2002:str", value)


Dumper.add_representer(str, _str_presenter)


def dump_yaml(obj):
    return yaml.dump(obj, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=10_000, default_flow_style=False)


def slugify(text, words=8):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    parts = re.findall(r"[a-z0-9]+", text.lower())
    return "-".join(parts[:words]) or "item"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pub_front_matter(p, aliases):
    cat = CATEGORY[p["type"]]
    fm = {
        "title": p["title"],
        "collection": "publications",
        "category": cat,
        "pub_id": p["id"],
        "number": p["number"],
        "permalink": f"/publication/{p['id'].lower()}-{slugify(p['title'])}/",
        "date": datetime.date(p["year"], 1, 1),
        "year": p["year"],
        # newest first: year, then journals before conferences, then the original numbering
        "sort_key": p["year"] * 1000 + (500 if p["type"] == "journal" else 0) + p["number"],
    }
    if p["type"] in ("journal", "conference"):
        fm["authors"] = p["authors"]
        if p["type"] == "journal":
            fm["venue"] = p["journal"]
            fm["venue_details"] = p["details"]
        else:
            fm["venue"] = p["venue"]
            if p.get("venue_short"):
                fm["venue_short"] = p["venue_short"]
            if p.get("workshop"):
                fm["workshop"] = True
        if p.get("online"):
            fm["online"] = True
        if p.get("award"):
            fm["award"] = p["award"]
        if p.get("doi"):
            fm["doi"] = p["doi"]
            fm["link"] = "https://doi.org/" + p["doi"]
    elif p["type"] == "patent":
        fm["authors"] = p["inventors"]
        fm["venue"] = f"{p['kind']} {p['publication_number']}"
        fm["venue_short"] = "Patent"
    elif p["type"] == "editorial":
        fm["authors"] = p["editors"]
        fm["venue"] = f"{p['event']}, {p['date_text']}, {p['location']}"
        fm["venue_short"] = "Proceedings"
    elif p["type"] == "thesis":
        fm["authors"] = ["K. Benabdeslem"]
        fm["venue"] = f"{p['document']}, {p['institution']}"
        fm["venue_short"] = p["degree"]
        fm["pages"] = p["pages"]
    fm["authors_text"] = ", ".join(fm["authors"])
    links = [l for l in p.get("links", []) if l["label"] != "DOI"]
    if links:
        fm["links"] = links
    fm["citation"] = esc(p["citation"])
    return fm


def write_publications(site):
    PUB_DIR.mkdir(exist_ok=True)
    for old in list(PUB_DIR.glob("*.md")) + list(PUB_DIR.glob("*.html")):
        old.unlink()
    aliases = site["meta"]["self_author_aliases"]
    pubs = site["publications"]
    n = 0
    for group in ("journals", "conferences", "patents", "editorial", "theses"):
        for p in pubs[group]:
            fm = pub_front_matter(p, aliases)
            name = f"{p['id'][0]}{p['number']:03d}-{slugify(p['title'], 6)}.html"
            body = "{% include pub-detail.html %}\n"
            (PUB_DIR / name).write_text("---\n" + dump_yaml(fm) + "---\n\n" + body, encoding="utf-8")
            n += 1
    return n


ROLE_ICONS = [("Lecturer", "fa-chalkboard-user"), ("Researcher", "fa-flask"), ("Co-head", "fa-people-group"),
              ("Responsible", "fa-graduation-cap"), ("Consultant", "fa-briefcase")]


def strip_source(items):
    return [{k: v for k, v in it.items() if k != "source_text"} for it in items]


def write_data(site):
    prof = site["profile"]
    roles = []
    for r in prof["roles"]:
        icon = next((i for k, i in ROLE_ICONS if r["text"].startswith(k)), "fa-circle")
        role = {"text": r["text"], "icon": icon}
        if r.get("link"):
            label = r["link"]["label"]
            before, _, after = r["text"].partition(label)
            role.update({"before": before, "link_label": label, "link": r["link"]["url"], "after": after})
        roles.append(role)
    announcements = []
    for a in prof["announcements"]:
        item = {k: v for k, v in a.items() if k != "source_text"}
        item["text"] = a["source_text"].lstrip("- ").strip()
        if isinstance(item.get("link"), dict):
            item["link_label"] = item["link"]["label"]
            item["link"] = item["link"]["url"]
        announcements.append(item)
    profile = {
        "name": prof["name"],
        "position": prof["position"],
        "self_aliases": site["meta"]["self_author_aliases"],
        "roles": roles,
        "research": site["research"],
        "announcements": announcements,
    }

    def student(s):
        d = {k: v for k, v in s.items() if k != "source_text"}
        d["start_year"] = int(s["start"][:4])
        d["end_year"] = int(s["end"][:4]) if s["end"] else None
        return d

    students = {k: ([student(s) for s in v] if isinstance(v, list) else v) for k, v in site["students"].items()}

    projects = strip_source(site["projects"])
    lo = min(p["start_year"] for p in projects)
    hi = max(p["end_year"] for p in projects) + 1
    span = hi - lo
    for p in projects:
        p["left"] = round((p["start_year"] - lo) / span * 100, 2)
        p["width"] = round((p["end_year"] - p["start_year"] + 1) / span * 100, 2)
    ticks = list(range(lo, hi + 1, 4)) if (hi - lo) % 4 == 0 else list(range(lo, hi + 1, 4)) + [hi]
    projects_data = {
        "timeline": {"from": lo, "to": hi,
                     "ticks": [{"year": y, "left": round((y - lo) / span * 100, 2)} for y in ticks]},
        "current": [p for p in projects if p["status"] == "current"],
        "past": [p for p in projects if p["status"] == "past"],
    }

    teaching = [{"institution": g["institution"], "courses": strip_source(g["courses"])} for g in site["teaching"]]

    cv = {
        "diplomas": strip_source(site["cv"]["diplomas"]),
        "experience": strip_source(site["cv"]["experience"]),
        "responsibilities": {k: strip_source(v) for k, v in site["responsibilities"].items()},
    }

    soft = []
    for s in site["unlisted_pages"]["software"]:
        d = {k: v for k, v in s.items() if k != "source_text"}
        soft.append(d)
    resources = {"links": site["links"], "software": soft}

    c = site["contact"]
    user, domain = c["email"].split("@")
    contact = {
        "organization": c["organization"],
        "address_lines": c["address_lines"],
        "phone": c["phone"],
        "fax": c["fax"],
        "email_user": user,
        "email_domain": domain,
        "email_display": c["email_display"],
        "website": c["website"],
        "access_map": c["map_image"]["link"],
    }

    files = {
        "profile.yml": profile, "students.yml": students, "projects.yml": projects_data, "teaching.yml": teaching,
        "cv.yml": cv, "resources.yml": resources, "contact.yml": contact,
        "archive_2010.yml": site["unlisted_pages"]["archive_2010"],
    }
    header = "# Generated by scripts/json_to_site.py from scripts/benabdeslem-site-data.json — edit the JSON and re-run, or edit here directly.\n"
    for name, obj in files.items():
        (DATA_DIR / name).write_text(header + dump_yaml(obj), encoding="utf-8")
    return list(files)


if __name__ == "__main__":
    site = json.loads(SRC.read_text(encoding="utf-8"))
    n = write_publications(site)
    names = write_data(site)
    print(f"wrote {n} publications and _data/{{{', '.join(names)}}}")
