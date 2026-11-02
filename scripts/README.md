# scripts/

## `json_to_site.py`

Rebuilds the site's content files from `benabdeslem-site-data.json` (the data migrated from the old website):

- `_publications/*.html` — one file per publication (the folder is emptied first)
- `_data/profile.yml`, `students.yml`, `projects.yml`, `teaching.yml`, `cv.yml`, `resources.yml`, `contact.yml`, `archive_2010.yml`

```
pip install pyyaml
python3 scripts/json_to_site.py
```

Pages in `_pages/` are never modified. This folder is excluded from the Jekyll build.
