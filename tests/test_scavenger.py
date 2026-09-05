"""Offline contract tests; these do not evaluate live research or agent behavior."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import scavenger as s


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "examples/demo-record.json").read_text())
        self.candidate = self.record["candidates"][0]

    def bad(self, expected):
        with self.assertRaisesRegex(s.Invalid, expected):
            s.validate(self.record)

    def test_valid_handoff(self):
        self.assertEqual(s.validate(self.record)["project"]["mode"], "handoff")

    def test_valid_draft_template(self):
        s.validate(s.load(ROOT / "assets/research-record.json"))

    def test_weighted_score(self):
        self.assertEqual(sum(s.WEIGHTS.values()), 100)
        self.assertEqual(s.score(self.record)[0]["score"], 84)

    def test_unknown_license_never_ranked(self):
        row = s.score(self.record)[1]
        self.assertEqual(row["status"], "review-required")
        self.assertIsNone(row["score"])
        self.assertTrue(row["synthetic"])

    def test_failed_gate_never_ranked(self):
        self.record["candidates"][1]["gates"]["security"] = "fail"
        self.assertEqual(s.score(self.record)[1]["status"], "blocked")

    def test_unknown_gate_blocks_adoption(self):
        self.candidate["gates"]["license"] = "unknown"
        self.bad("reuse blocked")

    def test_missing_dimension_rejected(self):
        del self.candidate["scores"]["maintenance"]
        self.bad("missing score dimensions")

    def test_invalid_ratings_rejected(self):
        original = copy.deepcopy(self.record)
        for value in (-1, 6, True, "5", 2.5, float("nan")):
            with self.subTest(value=value):
                self.record = copy.deepcopy(original)
                self.record["candidates"][0]["scores"]["integration"] = value
                self.bad("integer 0-5 or null")

    def test_null_rating_not_silently_imputed(self):
        self.record["decisions"][0]["disposition"] = "reference-only"
        self.candidate["scores"]["integration"] = None
        row = next(row for row in s.score(self.record) if row["id"] == "C-001")
        self.assertEqual(row["status"], "unscored")
        self.assertIsNone(row["score"])

    def test_unknown_rating_blocks_adoption(self):
        self.candidate["scores"]["integration"] = None
        self.bad("complete scores")

    def test_duplicate_requirement(self):
        self.record["requirements"].append(copy.deepcopy(self.record["requirements"][0]))
        self.bad("duplicate id")

    def test_unknown_evidence_source(self):
        self.candidate["evidence"][0]["source_id"] = "missing"
        self.bad("unknown reference")

    def test_unsupported_gate_note(self):
        self.candidate["gate_notes"]["license"]["source_ids"] = []
        self.bad("at least one reference")

    def test_unsupported_score_note(self):
        self.candidate["score_notes"]["requirement_fit"]["reason"] = " "
        self.bad("nonempty text")

    def test_undisposed_requirement(self):
        self.record["decisions"] = []
        self.bad("every requirement needs a disposition")

    def test_duplicate_disposition(self):
        self.record["decisions"].append(copy.deepcopy(self.record["decisions"][0]))
        self.bad("duplicate disposition")

    def test_missing_search_log(self):
        self.record["query_log"] = []
        self.bad("query_log is required")

    def test_discovery_cannot_support_reuse(self):
        self.candidate["evidence"][0]["level"] = "discovered"
        self.bad("code-inspected or tested")

    def test_tested_claim_requires_execution_record(self):
        self.candidate["evidence"][0]["level"] = "tested"
        self.bad("expected an object")
        self.candidate["evidence"][0]["test"] = {
            "command": "synthetic test command", "environment": "fixture only",
            "revision": "fixture-r1", "result": "synthetic pass; not actually executed"}
        s.validate(self.record)

    def test_placeholder_sources_require_synthetic_flag(self):
        self.record["project"]["synthetic"] = False
        self.bad("placeholder host")

    def test_dates_and_urls(self):
        original = copy.deepcopy(self.record)
        for field, value, error in (
            ("accessed_on", "2026-02-30", "invalid calendar date"),
            ("accessed_on", "2027-01-01", "after project.as_of"),
            ("url", "http://components.example/source", "HTTPS"),
            ("url", "https://user:secret@components.example/source", "credentials"),
            ("url", "https://components.example/source?token=secret", "query parameters"),
        ):
            with self.subTest(value=value):
                self.record = copy.deepcopy(original)
                self.record["sources"][0][field] = value
                self.bad(error)

    def test_explicit_gap_is_allowed(self):
        self.record["decisions"][0].update(disposition="gap", candidate_ids=[], rationale="No verified fit; further research required.")
        s.validate(self.record)

    def test_evidence_must_map_to_candidate_requirement(self):
        self.candidate["evidence"][0]["requirement_ids"] = ["REQ-MISSING"]
        self.bad("unknown reference")

    def test_empty_handoff_is_rejected(self):
        record = s.load(ROOT / "assets/research-record.json")
        record["project"]["mode"] = "handoff"
        with self.assertRaisesRegex(s.Invalid, "at least one requirement"):
            s.validate(record)


class HelperTests(unittest.TestCase):
    def test_skill_structure(self):
        s.check_skill(ROOT)

    def test_init_never_overwrites(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp).resolve() / "project"
            s.init_run(destination, "My project")
            s.validate(s.load(destination / "research-record.json"))
            with self.assertRaises(FileExistsError):
                s.init_run(destination, "Overwrite attempt")
            self.assertEqual(s.load(destination / "research-record.json")["project"]["name"], "My project")

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "record.json"
            path.write_text('{"project": 1, "project": 2}')
            with self.assertRaisesRegex(s.Invalid, "duplicate key"):
                s.load(path)

    def test_oversized_json_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "record.json"
            path.write_text(" " * (s.MAX_BYTES + 1))
            with self.assertRaisesRegex(s.Invalid, "2 MB"):
                s.load(path)

    def test_cli_reports_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "record.json"
            for payload in ("null", "[]", "{broken", '{"schema_version":"0.1","project":null}'):
                path.write_text(payload)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(s.main(["validate", str(path)]), 2)
                self.assertIn("ERROR:", stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_broken_skill_link_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            content = (ROOT / "SKILL.md").read_text()
            (root / "SKILL.md").write_text(content)
            with self.assertRaisesRegex(s.Invalid, "invalid local link"):
                s.check_skill(root)


if __name__ == "__main__":
    unittest.main()
