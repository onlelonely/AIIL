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

This site is intended to deploy as a static site on **Cloudflare Pages**.

Recommended Cloudflare Pages settings:

- Framework preset: `None`
- Build command: none
- Build output directory: `/`
- Production branch: `main`

## Validation

Desktop and mobile visual checks can be run with Playwright against a local preview server.
