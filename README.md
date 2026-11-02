# Khalid Benabdeslem — academic website

Personal academic website built on the [Academic Pages](https://github.com/academicpages/academicpages.github.io) Jekyll template and hosted for free on GitHub Pages. All content was migrated from the previous site (kbenabde.free.fr/bk).

**What's inside**

| Page | URL | Content comes from |
|---|---|---|
| Home | `/` | `_pages/about.html` + `_data/profile.yml` |
| Research | `/research/` | `_data/profile.yml` → `research` |
| Publications | `/publications/` | `_publications/*.html` (123 files: 24 journals, 91 conferences, 1 patent, 3 proceedings, 4 theses) |
| Students | `/students/` | `_data/students.yml` |
| Projects | `/projects/` | `_data/projects.yml` |
| Teaching | `/teaching/` | `_data/teaching.yml` |
| CV | `/cv/` | `_data/cv.yml` |
| Resources | `/resources/` | `_data/resources.yml` (links + software) |
| Positions & news | `/positions/` | `_data/profile.yml` → `announcements`, `_data/archive_2010.yml` |
| Contact | `/contact/` | `_data/contact.yml` |

Extras: searchable/filterable publication list with a per-year chart, project timeline, light/dark mode (sun/moon icon in the menu), print-friendly CV, mobile layout.

---

## Publish it on GitHub Pages

1. **Create a repository** on GitHub.
   - For `https://<username>.github.io`, name it exactly `<username>.github.io`.
   - Any other name also works; the site is then served at `https://<username>.github.io/<repo-name>/`.
2. **Push these files** (everything in this folder, including the hidden `.github` folder and `.gitignore`) to the `main` (or `master`) branch:
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```
3. **Turn on Pages**: in the repository go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
4. The workflow in `.github/workflows/jekyll.yml` builds and deploys the site on every push. Follow it under the **Actions** tab; the first run takes about 2–3 minutes.
5. *(Optional)* In `_config.yml`, set `url: "https://<username>.github.io"` and `repository: "<username>/<repo>"` so the sitemap and social previews use absolute links. Leaving `url` empty works fine.

## Edit the content

- **Small changes**: edit the YAML files in `_data/` or a file in `_publications/` directly on GitHub (pencil icon) and commit; the site rebuilds automatically.
- **Add a publication**: copy an existing file in `_publications/` (e.g. `J024-...html`), give it a new name and update the fields (`pub_id`, `number`, `title`, `authors`, `venue`, `year`, `sort_key`, `category` = `journals` / `conferences` / `patents` / `editorial` / `theses`). Add `doi:` and `link:` for a DOI button, or `award:` for a trophy badge.
- **Bulk regeneration**: all content files can be rebuilt from the migrated data in `scripts/benabdeslem-site-data.json`:
  ```bash
  pip install pyyaml
  python3 scripts/json_to_site.py
  ```
  This rewrites `_publications/` and the YAML files in `_data/` (not the pages in `_pages/`), so do it before making hand edits to those files, or edit the JSON instead.
- **Biography text** on the home page lives in `_pages/about.html`.
- **Menu**: `_data/navigation.yml`.
- **Profile picture**: put a photo in `images/` (e.g. `images/profile.jpg`) and set `avatar: "profile.jpg"` in `_config.yml` (the current one is a "KB" monogram).
- **Academic profiles**: fill `googlescholar`, `orcid`, `researchgate`, `linkedin`… under `author:` in `_config.yml` to show them in the sidebar.
- **Colours**: change `site_theme` in `_config.yml` (`default`, `air`, `sunrise`, `mint`, `dirt`, `contrast`); the custom components in `_sass/layout/_kb.scss` follow the theme colours automatically.

## Run it locally (optional)

Requires Ruby 3.x and Node.js.

```bash
bundle install
npm install && npm run build:js   # builds assets/js/main.min.js (done automatically on GitHub)
bundle exec jekyll serve -l -H localhost
```
Then open http://localhost:4000.

## Notes from the migration

- Text was kept exactly as on the original site. A few inconsistencies were spotted and left for you to decide on: papers C87, C90 and C91 spell the author "Y. Lairigi" while the Students page says "Yassir Lairgi"; the AGS'09 proceedings (E1) are dated May 2011; some typos ("Muti-modal", "Crowdsoursing", "uncertainlty", "Reasonning").
- The e-mail address is assembled by JavaScript on the Contact page (the old site also hid it from spam bots) and is not shown in the sidebar.
- Links to the old `kbenabdeslem.free.fr` software files were kept as they were; some may no longer work.

Theme: [Academic Pages](https://github.com/academicpages/academicpages.github.io) (MIT licence), a fork of [Minimal Mistakes](https://mademistakes.com/work/minimal-mistakes-jekyll-theme/).
