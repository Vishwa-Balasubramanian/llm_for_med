"""Load report metadata and constrain source paths to the dataset root."""

from pathlib import Path

from clinical_events.data.jsonl import read_jsonl
from clinical_events.schemas.report import Report


def load_reports(manifest: Path) -> list[Report]:
    reports = []
    for row, values in enumerate(read_jsonl(manifest), start=1):
        try:
            reports.append(Report.from_dict(values))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"report record {row}: {exc}") from exc
    return reports


def resolve_source(root: Path, report: Report) -> Path:
    root = root.resolve()
    source = (root / report.source_path).resolve()
    if not source.is_relative_to(root):
        raise ValueError(f"{report.report_id}: source resolves outside dataset root")
    return source

