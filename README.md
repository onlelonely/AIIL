# AIIL

Static bilingual homepage for the AI-Assisted Immunoinformatics Lab at NPUST.

## Structure

- `index.html`: homepage
- `collaborators.html`: collaborators, funding and lab members
- `publications.html`: featured papers, full list, manuscripts under review, talks; citations and the list are rendered in the browser from `data/publications.json`
- `site.js`: language switch and pen strokes for the sub-pages (each page defines `window.I18N` first)
- `site.css`: styles shared by all pages (tokens, top bar, section labels, colophon); page-specific rules stay inline in each page
- `profile.jpg`: PI portrait
- `claude_content_collection_prompt.md`: content collection prompt for Claude-based research or writing workflows

## Local Preview

```bash
python3 -m http.server 4173
```

Then open [http://127.0.0.1:4173](http://127.0.0.1:4173).

## Deployment

Deployed as a static site on **Cloudflare Pages** (project `aiil`, Git-connected to `onlelonely/AIIL`). Every push to `main` deploys automatically.

- Live: <https://aiil.science> (`www.aiil.science` 301-redirects to the apex via a zone Redirect Rule)
- Pages preview: <https://aiil.pages.dev>
- Framework preset: `None`
- Build command: none
- Build output directory: repo root (left blank)
- Production branch: `main`

Everything in the repo root is published, so keep tooling folders such as `.claude/` out of this repo.

## Publications

`data/publications.json` is generated from ORCID [0000-0002-1126-7697](https://orcid.org/0000-0002-1126-7697) (journal articles only), enriched with Crossref (volume, issue, pages, author list, author position). Do not edit it by hand.

- Hand-maintained fields go in `data/publications.overrides.json`, keyed by lowercase DOI: `short_title_zh`, `short_title_en`, `note_zh`, `note_en`, `journal_abbrev`, `role`, `hidden`, etc. Overrides win over fetched values.
- `.github/workflows/publications.yml` rebuilds weekly (Mon 09:17 Taipei) and on manual dispatch, then commits if the file changed; that push redeploys Cloudflare Pages.
- New works without `short_title_zh` are listed under the run's summary as "needs short_title_zh".
- The build refuses to publish an empty list or one that shrank by half (ORCID outage guard); dispatch with `allow_shrink` if a large removal is intended.

```bash
python3 -m unittest discover -s scripts   # offline tests
python3 scripts/build_publications.py     # rebuild locally
```

## Validation

Desktop and mobile visual checks can be run with Playwright against a local preview server.
