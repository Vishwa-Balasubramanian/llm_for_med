"""Structural checks and dataset readiness indicators, not de-identification."""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

from clinical_events.data.load_reports import resolve_source
from clinical_events.schemas.report import Report


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict = field(default_factory=dict)


def validate_reports(reports: list[Report], root: Path) -> ValidationResult:
    result = ValidationResult()
    if not reports:
        result.errors.append("Dataset is empty")
    ids = Counter(report.report_id for report in reports)
    result.errors.extend(f"Duplicate report_id: {key}" for key, count in ids.items() if count > 1)
    patient_dates = defaultdict(set)
    patients = set()
    hashes = {}
    for report in reports:
        patients.add(report.patient_id)
        if report.exam_date is None:
            result.warnings.append(f"{report.report_id}: unknown examination date; excluded from dated timeline")
        else:
            patient_dates[report.patient_id].add(report.exam_date)
        try:
            source = resolve_source(root, report)
            if not source.is_file():
                raise ValueError(f"{report.report_id}: source file is missing")
            content = source.read_bytes()
            if not content:
                raise ValueError(f"{report.report_id}: source file is empty")
            if source.suffix.lower() == ".txt" and not content.decode("utf-8-sig").strip():
                raise ValueError(f"{report.report_id}: report text is blank")
            if source.suffix.lower() == ".pdf" and not content.startswith(b"%PDF-"):
                raise ValueError(f"{report.report_id}: file does not have a PDF header")
            digest = sha256(content).hexdigest()
            if digest in hashes:
                result.warnings.append(f"{report.report_id}: identical source bytes to {hashes[digest]}")
            hashes[digest] = report.report_id
        except (OSError, ValueError) as exc:
            result.errors.append(str(exc))
    longitudinal = sum(len(dates) >= 2 for dates in patient_dates.values())
    if longitudinal < len(patients):
        result.warnings.append("Some patients have fewer than two distinct examination dates")
    synthetic_count = sum(report.is_synthetic for report in reports)
    if synthetic_count:
        result.warnings.append("Synthetic reports are for software demonstrations, not clinical evaluation")
    result.summary = {
        "reports": len(reports),
        "patients": len(patients),
        "patients_with_multiple_dates": longitudinal,
        "reports_with_unknown_date": sum(report.exam_date is None for report in reports),
        "synthetic_reports": synthetic_count,
    }
    return result

