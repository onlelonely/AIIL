#!/usr/bin/env python3
"""Build data/publications.json from ORCID, enriched with Crossref.

Stdlib only, so the GitHub Action needs no install step.

    python3 scripts/build_publications.py            # write data/publications.json
    python3 scripts/build_publications.py --check    # fetch and validate, write nothing

Hand-maintained fields (short zh/en titles, notes, role exceptions,
hidden works) live in data/publications.overrides.json, keyed by lowercase DOI.
Overrides always win over fetched values.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORCID_ID = "0000-0002-1126-7697"
SELF_GIVEN = "li-hsin"
SELF_FAMILY = "chang"
INCLUDED_TYPES = {"journal-article"}

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "publications.json"
OVERRIDES_PATH = ROOT / "data" / "publications.overrides.json"

USER_AGENT = "AIIL-publications-sync/1.0 (+https://aiil.science)"
TIMEOUT = 30


def http_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def normalize_doi(doi):
    doi = (doi or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi


def _value(node, *keys):
    for key in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def _iso(parts):
    """[[2023, 8, 1]] -> '2023-08-01'; tolerates missing month/day."""
    if not parts or not parts[0] or parts[0][0] is None:
        return None
    return "-".join(f"{p:02d}" if i else str(p) for i, p in enumerate(parts[0]))


def orcid_works(orcid_id=ORCID_ID):
    """One summary per ORCID work group: the one the owner ranked highest."""
    data = http_json(f"https://pub.orcid.org/v3.0/{orcid_id}/works", {"Accept": "application/json"})
    works = []
    for group in data.get("group", []):
        summary = max(group["work-summary"], key=lambda s: int(s.get("display-index") or 0))
        if summary.get("type") not in INCLUDED_TYPES:
            continue
        ids = {
            e["external-id-type"]: e["external-id-value"]
            for e in _value(summary, "external-ids", "external-id") or []
        }
        date = summary.get("publication-date") or {}
        date_parts = [int(v["value"]) for k in ("year", "month", "day") if (v := date.get(k))]
        works.append({
            "doi": normalize_doi(ids.get("doi")),
            "title": _value(summary, "title", "title", "value"),
            "journal": _value(summary, "journal-title", "value"),
            "date": _iso([date_parts]) if date_parts else None,
            "orcid_put_code": summary["put-code"],
        })
    return works


def crossref_work(doi):
    return http_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")["message"]


def is_self(author):
    if author.get("ORCID", "").endswith(ORCID_ID):
        return True
    given = (author.get("given") or "").strip().lower().replace(" ", "-")
    return given == SELF_GIVEN and (author.get("family") or "").strip().lower() == SELF_FAMILY


def from_crossref(msg):
    """Pick the citation fields we display from a Crossref record."""
    authors = msg.get("author") or []
    position = next((i + 1 for i, a in enumerate(authors) if is_self(a)), None)
    # Citation year follows the print issue when there is one (Cell Mol Neurobiol
    # was online 2022-12 but is cited as 2023;43(6)).
    print_date = _iso(_value(msg, "published-print", "date-parts"))
    online_date = _iso(_value(msg, "published-online", "date-parts")) or _iso(_value(msg, "issued", "date-parts"))
    short = msg.get("short-container-title") or []
    return {
        "title": (msg.get("title") or [None])[0],
        "journal": (msg.get("container-title") or [None])[0],
        "journal_abbrev": short[0] if short else None,
        "volume": msg.get("volume"),
        "issue": msg.get("issue"),
        "pages": msg.get("page") or msg.get("article-number"),
        "year": int((print_date or online_date)[:4]) if (print_date or online_date) else None,
        "date": online_date or print_date,
        "authors": [" ".join(filter(None, (a.get("given"), a.get("family")))) or a.get("name") for a in authors],
        "author_position": position,
        "author_count": len(authors),
        "role": "first-author" if position == 1 else "co-author",
    }


def build(works, crossref, previous, overrides):
    """Merge ORCID works, Crossref records and overrides into the published list.

    works: ORCID summaries. crossref: doi -> Crossref message, or None when the
    lookup failed. previous: doi -> entry from the last published file, reused
    when Crossref is unavailable so a flaky lookup never degrades the page.
    """
    entries, warnings = [], []
    for work in works:
        doi = work["doi"]
        entry = {"doi": doi or None, "url": f"https://doi.org/{doi}" if doi else None,
                 "orcid_put_code": work["orcid_put_code"], "title": work["title"],
                 "journal": work["journal"], "date": work["date"],
                 "year": int(work["date"][:4]) if work["date"] else None}
        if not doi:
            warnings.append(f"no DOI on ORCID put-code {work['orcid_put_code']}: {work['title']}")
        elif crossref.get(doi):
            entry.update({k: v for k, v in from_crossref(crossref[doi]).items() if v not in (None, "", [])})
        elif doi in previous:
            entry = {**previous[doi], **{k: v for k, v in entry.items() if k == "orcid_put_code"}}
            warnings.append(f"Crossref unavailable for {doi}; kept last published record")
        else:
            warnings.append(f"Crossref unavailable for {doi}; using ORCID fields only")

        override = overrides.get(doi, {})
        entry.update(override)
        if entry.pop("hidden", False):
            continue
        if doi and "short_title_zh" not in override:
            warnings.append(f"needs short_title_zh: {doi} ({entry.get('title')})")
        entries.append(entry)

    for doi in overrides.keys() - {w["doi"] for w in works}:
        warnings.append(f"override for {doi} matches no ORCID work")

    entries.sort(key=lambda e: (e.get("date") or "", e.get("doi") or ""), reverse=True)
    return entries, warnings


def check_shrink(new_count, old_count):
    """Refuse to publish an empty or sharply shorter list (ORCID outage, API change)."""
    if new_count == 0:
        return "ORCID returned no works"
    if old_count and new_count < old_count * 0.5:
        return f"work count fell from {old_count} to {new_count}"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fetch and validate without writing")
    parser.add_argument("--allow-shrink", action="store_true", help="publish even if the list got much shorter")
    args = parser.parse_args()

    overrides = {normalize_doi(k): v for k, v in json.loads(OVERRIDES_PATH.read_text()).items() if not k.startswith("_")}
    previous_doc = json.loads(OUT_PATH.read_text()) if OUT_PATH.exists() else {"works": []}
    previous = {e["doi"]: e for e in previous_doc["works"] if e.get("doi")}

    works = orcid_works()
    crossref = {}
    for work in works:
        if not work["doi"]:
            continue
        try:
            crossref[work["doi"]] = crossref_work(work["doi"])
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
            print(f"warning: Crossref lookup failed for {work['doi']}: {exc}", file=sys.stderr)
            crossref[work["doi"]] = None

    entries, warnings = build(works, crossref, previous, overrides)
    problem = check_shrink(len(entries), len(previous_doc["works"]))
    if problem and not args.allow_shrink:
        sys.exit(f"error: {problem}; refusing to overwrite {OUT_PATH.name} (use --allow-shrink if intended)")

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path and warnings:
        with open(summary_path, "a") as fh:
            fh.write("### Publications sync warnings\n\n" + "".join(f"- {w}\n" for w in warnings))

    doc = {"orcid": ORCID_ID, "source": f"https://orcid.org/{ORCID_ID}", "works": entries}
    text = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        print(f"ok: {len(entries)} works (not written)")
        return
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(text)
    print(f"wrote {len(entries)} works to {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
