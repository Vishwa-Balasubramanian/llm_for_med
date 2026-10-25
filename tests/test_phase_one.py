"""Behavioral tests for data integrity and leakage prevention."""

from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from clinical_events.data.load_reports import load_reports, resolve_source
from clinical_events.data.split_patients import split_patients
from clinical_events.data.validate_annotations import validate_annotations
from clinical_events.data.validate_reports import validate_reports
from clinical_events.schemas.report import Report


EXAMPLES = Path(__file__).resolve().parents[1] / "data" / "examples"


class PhaseOneTests(unittest.TestCase):
    def setUp(self):
        self.reports = load_reports(EXAMPLES / "reports.jsonl")

    def test_examples_have_longitudinal_coverage(self):
        result = validate_reports(self.reports, EXAMPLES)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["patients_with_multiple_dates"], 3)

    def test_example_annotations_have_exact_evidence(self):
        result = validate_annotations(EXAMPLES / "annotations.jsonl", self.reports, EXAMPLES)
        self.assertEqual(result.errors, [])
        self.assertTrue(result.warnings)  # Synthetic labels remain draft.

    def test_duplicate_report_ids_fail(self):
        result = validate_reports(self.reports + [self.reports[0]], EXAMPLES)
        self.assertTrue(any("Duplicate report_id" in error for error in result.errors))

    def test_missing_source_fails(self):
        report = replace(self.reports[0], source_path="reports/missing.txt")
        self.assertTrue(validate_reports([report], EXAMPLES).errors)

    def test_unknown_date_is_preserved_and_flagged(self):
        report = replace(self.reports[0], exam_date=None)
        result = validate_reports([report], EXAMPLES)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["reports_with_unknown_date"], 1)

    def test_invalid_calendar_date_fails(self):
        from dataclasses import asdict
        values = asdict(self.reports[0])
        values["exam_date"] = "2024-02-30"
        with self.assertRaises(ValueError):
            Report.from_dict(values)

    def test_path_traversal_fails(self):
        from dataclasses import asdict
        values = asdict(self.reports[0])
        values["source_path"] = "../outside.txt"
        with self.assertRaises(ValueError):
            Report.from_dict(values)
        with self.assertRaises(ValueError):
            resolve_source(EXAMPLES, replace(self.reports[0], source_path="../outside.txt"))

    def test_splits_are_disjoint_and_order_independent(self):
        groups = split_patients(self.reports)
        self.assertEqual(groups, split_patients(list(reversed(self.reports))))
        flattened = [patient for patients in groups.values() for patient in patients]
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertEqual(set(flattened), {report.patient_id for report in self.reports})
        self.assertTrue(all(groups.values()))

    def test_small_cohort_cannot_make_three_splits(self):
        with self.assertRaises(ValueError):
            split_patients(self.reports[:1])

    def test_modified_evidence_is_rejected(self):
        record = json.loads((EXAMPLES / "annotations.jsonl").read_text().splitlines()[0])
        record["evidence_text"] = "Unsupported text."
        with TemporaryDirectory() as folder:
            path = Path(folder) / "annotations.jsonl"
            path.write_text(json.dumps(record), encoding="utf-8")
            result = validate_annotations(path, self.reports, EXAMPLES)
            self.assertTrue(any("evidence" in error for error in result.errors))

    def test_cross_patient_finding_link_is_rejected(self):
        records = [json.loads(line) for line in (EXAMPLES / "annotations.jsonl").read_text().splitlines()]
        first = records[0]
        other = next(record for record in records if record["report_id"].startswith("SYN002"))
        other["finding_id"] = first["finding_id"]
        with TemporaryDirectory() as folder:
            path = Path(folder) / "annotations.jsonl"
            path.write_text("\n".join(json.dumps(record) for record in [first, other]), encoding="utf-8")
            result = validate_annotations(path, self.reports, EXAMPLES)
            self.assertTrue(any("different patients" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()

