"""Offline tests for build_publications.py: python3 -m unittest discover scripts"""

import unittest

from build_publications import build, check_shrink, from_crossref, normalize_doi

SELF = {"given": "Li-Hsin", "family": "Chang", "sequence": "first"}
OTHER = {"given": "Nai-Fang", "family": "Chi", "sequence": "additional"}


def crossref(**extra):
    msg = {
        "title": ["Monogenic Causes in Familial Stroke"],
        "container-title": ["Cellular and Molecular Neurobiology"],
        "short-container-title": ["Cell Mol Neurobiol"],
        "volume": "43", "issue": "6", "page": "2769-2783",
        "published-print": {"date-parts": [[2023, 8]]},
        "published-online": {"date-parts": [[2022, 12, 29]]},
        "author": [SELF, OTHER],
    }
    msg.update(extra)
    return msg


def work(doi="10.1007/x", date="2022-12-29"):
    return {"doi": doi, "title": "ORCID title", "journal": "ORCID journal", "date": date, "orcid_put_code": 1}


class NormalizeDoi(unittest.TestCase):
    def test_strips_prefix_and_lowercases(self):
        self.assertEqual(normalize_doi("https://doi.org/10.1212/WNL.0000000000218126"), "10.1212/wnl.0000000000218126")
        self.assertEqual(normalize_doi(None), "")


class FromCrossref(unittest.TestCase):
    def test_print_year_wins_over_online_date(self):
        rec = from_crossref(crossref())
        self.assertEqual(rec["year"], 2023)
        self.assertEqual(rec["date"], "2022-12-29")

    def test_online_only_record(self):
        rec = from_crossref(crossref(**{"published-print": None, "published-online": {"date-parts": [[2026, 10, 13]]}}))
        self.assertEqual(rec["year"], 2026)

    def test_role_from_author_position(self):
        self.assertEqual(from_crossref(crossref())["role"], "first-author")
        rec = from_crossref(crossref(author=[OTHER, {**SELF, "sequence": "additional"}]))
        self.assertEqual((rec["role"], rec["author_position"], rec["author_count"]), ("co-author", 2, 2))

    def test_self_matched_by_orcid_even_if_name_differs(self):
        me = {"given": "L.-H.", "family": "Chang", "ORCID": "https://orcid.org/0000-0002-1126-7697"}
        self.assertEqual(from_crossref(crossref(author=[me, OTHER]))["author_position"], 1)

    def test_article_number_when_no_page(self):
        self.assertEqual(from_crossref(crossref(page=None, **{"article-number": "e218126"}))["pages"], "e218126")


class Build(unittest.TestCase):
    def test_override_wins_and_hidden_is_dropped(self):
        works = [work("10.1/a"), work("10.1/b")]
        entries, _ = build(works, {"10.1/a": crossref(), "10.1/b": crossref()}, {},
                           {"10.1/a": {"role": "co-first-author", "short_title_zh": "甲"}, "10.1/b": {"hidden": True}})
        self.assertEqual([e["doi"] for e in entries], ["10.1/a"])
        self.assertEqual(entries[0]["role"], "co-first-author")
        self.assertNotIn("hidden", entries[0])

    def test_crossref_outage_reuses_previous_record(self):
        previous = {"10.1/a": {"doi": "10.1/a", "volume": "43", "orcid_put_code": 1}}
        entries, warnings = build([work("10.1/a")], {"10.1/a": None}, previous, {"10.1/a": {"short_title_zh": "甲"}})
        self.assertEqual(entries[0]["volume"], "43")
        self.assertTrue(any("kept last published record" in w for w in warnings))

    def test_warns_on_missing_zh_title_and_orphan_override(self):
        _, warnings = build([work("10.1/a")], {"10.1/a": crossref()}, {}, {"10.1/gone": {"short_title_zh": "乙"}})
        self.assertTrue(any("needs short_title_zh: 10.1/a" in w for w in warnings))
        self.assertTrue(any("10.1/gone matches no ORCID work" in w for w in warnings))

    def test_sorted_newest_first(self):
        works = [work("10.1/old", "2017-05-16"), work("10.1/new", "2026-06-23")]
        entries, _ = build(works, {}, {}, {})
        self.assertEqual([e["doi"] for e in entries], ["10.1/new", "10.1/old"])


class CheckShrink(unittest.TestCase):
    def test_guards(self):
        self.assertIsNotNone(check_shrink(0, 0))
        self.assertIsNotNone(check_shrink(4, 9))
        self.assertIsNone(check_shrink(8, 9))
        self.assertIsNone(check_shrink(9, 0))


if __name__ == "__main__":
    unittest.main()
