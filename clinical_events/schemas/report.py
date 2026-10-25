"""Input metadata. Source text remains in its original document."""

from dataclasses import dataclass
from datetime import date
from pathlib import PurePosixPath
import re


@dataclass(frozen=True)
class Report:
    patient_id: str
    report_id: str
    exam_date: str | None
    source_path: str
    report_type: str
    language: str
    is_synthetic: bool
    modality: str | None = None
    body_region: str | None = None

    @classmethod
    def from_dict(cls, values: dict) -> "Report":
        report = cls(**values)
        for name in ("patient_id", "report_id", "source_path", "report_type", "language"):
            value = getattr(report, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if type(report.is_synthetic) is not bool:
            raise ValueError("is_synthetic must be true or false")
        for name in ("modality", "body_region"):
            value = getattr(report, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be a non-empty string or null")
        if report.exam_date is not None:
            if not isinstance(report.exam_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", report.exam_date):
                raise ValueError("exam_date must be YYYY-MM-DD or null")
            date.fromisoformat(report.exam_date)
        path = PurePosixPath(report.source_path)
        if path.is_absolute() or ".." in path.parts or "\\" in report.source_path or ":" in report.source_path:
            raise ValueError("source_path must be a relative POSIX path within the dataset")
        if path.suffix.lower() not in {".txt", ".pdf"}:
            raise ValueError("source_path must reference a .txt or .pdf file")
        return report

