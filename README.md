# AIIL

Static bilingual homepage for the AI-Assisted Immunoinformatics Lab at NPUST.

## Structure

- `index.html`: single-page site
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

## Validation

Desktop and mobile visual checks can be run with Playwright against a local preview server.
