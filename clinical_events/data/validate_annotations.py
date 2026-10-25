"""Check annotation references and exact evidence against canonical TXT."""

from pathlib import Path

from clinical_events.data.jsonl import read_jsonl
from clinical_events.data.load_reports import resolve_source
from clinical_events.data.validate_reports import ValidationResult
from clinical_events.schemas.event import Event
from clinical_events.schemas.report import Report


def validate_annotations(path: Path, reports: list[Report], root: Path) -> ValidationResult:
    result = ValidationResult()
    by_id = {report.report_id: report for report in reports}
    event_ids = set()
    finding_owners = {}
    count = 0
    for row, values in enumerate(read_jsonl(path), start=1):
        try:
            event = Event.from_dict(values)
            count += 1
            if event.event_id in event_ids:
                raise ValueError(f"Duplicate event_id: {event.event_id}")
            event_ids.add(event.event_id)
            if event.report_id not in by_id:
                raise ValueError(f"{event.event_id}: unknown report_id")
            report = by_id[event.report_id]
            owner = finding_owners.setdefault(event.finding_id, report.patient_id)
            if owner != report.patient_id:
                raise ValueError(f"{event.event_id}: finding_id links different patients")
            source = resolve_source(root, report)
            if source.suffix.lower() != ".txt":
                raise ValueError(f"{event.event_id}: PDF evidence needs Phase 2 canonical text; not validated")
            text = source.read_text(encoding="utf-8-sig")
            if event.evidence_end > len(text) or text[event.evidence_start:event.evidence_end] != event.evidence_text:
                raise ValueError(f"{event.event_id}: evidence does not match source offsets")
            if event.review_status != "expert_reviewed":
                result.warnings.append(f"{event.event_id}: draft annotation; not an expert reference label")
        except (TypeError, ValueError, OSError) as exc:
            result.errors.append(f"annotation record {row}: {exc}")
    if count == 0:
        result.errors.append("No valid annotation records")
    result.summary = {"annotations": count}
    return result

