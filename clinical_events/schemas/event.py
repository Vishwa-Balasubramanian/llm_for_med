"""Annotation contract; no automated clinical interpretation happens here."""

from dataclasses import dataclass


CATEGORIES = {"tumor_metastasis", "complication", "procedure_device"}
ASSERTIONS = {"present", "absent", "uncertain"}
TEMPORAL_CONTEXTS = {"current", "historical", "planned", "unknown"}
CHANGES = {"new", "progressing", "regressing", "stable", "resolved", "not_stated"}
DEVICE_ACTIONS = {"present", "inserted", "removed", "planned", "not_applicable"}


@dataclass(frozen=True)
class Event:
    event_id: str
    report_id: str
    finding_id: str
    category: str
    finding: str
    anatomy: str | None
    laterality: str
    assertion: str
    temporal_context: str
    reported_change: str
    device_action: str
    evidence_text: str
    evidence_start: int
    evidence_end: int
    review_status: str

    @classmethod
    def from_dict(cls, values: dict) -> "Event":
        event = cls(**values)
        for name in ("event_id", "report_id", "finding_id", "finding", "evidence_text"):
            if not isinstance(getattr(event, name), str) or not getattr(event, name).strip():
                raise ValueError(f"{name} must be a non-empty string")
        allowed = {
            "category": CATEGORIES,
            "assertion": ASSERTIONS,
            "temporal_context": TEMPORAL_CONTEXTS,
            "reported_change": CHANGES,
            "device_action": DEVICE_ACTIONS,
            "laterality": {"left", "right", "bilateral", "midline", "unknown", "not_applicable"},
            "review_status": {"draft", "expert_reviewed"},
        }
        for name, choices in allowed.items():
            value = getattr(event, name)
            if not isinstance(value, str) or value not in choices:
                raise ValueError(f"{name} must be one of {sorted(choices)}")
        if event.anatomy is not None and (not isinstance(event.anatomy, str) or not event.anatomy.strip()):
            raise ValueError("anatomy must be a non-empty string or null")
        if type(event.evidence_start) is not int or type(event.evidence_end) is not int:
            raise ValueError("evidence offsets must be integers")
        if not 0 <= event.evidence_start < event.evidence_end:
            raise ValueError("evidence offsets must satisfy 0 <= start < end")
        return event

