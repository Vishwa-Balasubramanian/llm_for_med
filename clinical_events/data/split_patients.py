"""Deterministic patient-group splits. Freeze assignments before evaluation."""

from hashlib import sha256

from clinical_events.schemas.report import Report


def split_patients(reports: list[Report], seed: int = 42) -> dict[str, list[str]]:
    patients = sorted(
        {report.patient_id for report in reports},
        key=lambda patient: (sha256(f"{seed}:{patient}".encode()).hexdigest(), patient),
    )
    if len(patients) < 3:
        raise ValueError("At least three patients are needed for separate train/dev/test groups")
    # Approximate 60/20/20; preserve at least one patient in dev and test.
    n_dev = max(1, int(len(patients) * 0.2))
    n_test = max(1, int(len(patients) * 0.2))
    n_train = len(patients) - n_dev - n_test
    return {
        "train": patients[:n_train],
        "dev": patients[n_train:n_train + n_dev],
        "test": patients[n_train + n_dev:],
    }

