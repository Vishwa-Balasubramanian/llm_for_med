# Clinical Event Detection on Longitudinal Reports

Turn dated patient reports into an evidence-linked history of tumor/metastasis,
complications, and procedures/devices.

**Current stage: Phase 1 — data preparation and problem definition.**
Project-provided de-identified reports are selected but not available yet.
The included reports and annotations are synthetic demonstrations only.

## Repository structure

```text
clinical_events/
  schemas/                 Report and annotation contracts
    report.py
    event.py
  data/                    One responsibility per module
    jsonl.py               JSONL reader
    load_reports.py        Manifest loading and source resolution
    validate_reports.py    Metadata, dates, duplicates, source checks
    validate_annotations.py Exact evidence and patient-link checks
    split_patients.py      Deterministic patient-level splits
  cli/
    validate_dataset.py    Dataset validation command
    create_splits.py       Split creation command

data/
  examples/                Synthetic reports and draft annotations
  templates/               Empty manifest and intake checklist
  private/                 Real reports when available; Git-ignored
  processed/               Derived data; Git-ignored
  splits/                  Frozen patient assignments; Git-ignored

docs/phase_1/              Data contract, annotation guide, evaluation, status
output/                    Existing project architecture image
tests/                     Data-integrity and patient-isolation checks
```

The private, processed, and splits directories are created when needed.
Phase 1 uses only the Python standard library; no third-party installs are needed.
Later phases will introduce PDF/OCR, model, workflow, and interface dependencies.

## Environment

The local environment uses Python 3.14. From the repository in PowerShell:

```powershell
# Create only if .venv does not already exist:
py -3.14 -m venv .venv

# Optional activation:
.\.venv\Scripts\Activate.ps1
```

All commands below use the environment directly, so activation is not required.

## Validate the example dataset

```powershell
.\.venv\Scripts\python.exe -m clinical_events.cli.validate_dataset data/examples/reports.jsonl --annotations data/examples/annotations.jsonl
```

Expected: 9 reports, 3 patients with repeated dates, 27 draft annotations, no
validation errors. Warnings explicitly identify synthetic data and draft labels.
A nonzero exit code means validation failed. Passing these checks does not
establish clinical correctness or de-identification.

## Create patient-level splits

```powershell
.\.venv\Scripts\python.exe -m clinical_events.cli.create_splits data/examples/reports.jsonl --output data/splits/synthetic-v1.json
```

All reports for one patient stay together. The command refuses to overwrite an
existing split file. Use a new versioned filename only when intentionally making
new assignments. Three synthetic patients are enough for a software demonstration,
not for a clinical evaluation.

## Run checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## When the project reports arrive

1. Complete [the intake checklist](data/templates/intake_checklist.md).
2. Place authorized files in `data/private/project-v1/reports/`.
3. Create `data/private/project-v1/reports.jsonl` using the
   [data contract](docs/phase_1/data_contract.md), with `is_synthetic: false`.
4. Run validation against that manifest. Unknown dates remain unknown.
5. Review the [annotation guide](docs/phase_1/annotation_guidelines.md) with a
   qualified reviewer and annotate the development pilot.
6. Freeze patient-level splits and the [evaluation plan](docs/phase_1/evaluation_plan.md).

PDF source existence is supported now; PDF parsing, OCR, and evidence coordinates
are Phase 2. Exact annotation evidence checks currently require TXT sources.

## Five phases

1. Data collection, schemas, annotations, and evaluation design — in progress.
2. PDF/text processing and baseline event extraction.
3. Longitudinal linking and agent verification.
4. Timeline application, source viewer, and incremental updates.
5. Held-out evaluation, documentation, and final delivery.

See [Phase 1 status](docs/phase_1/status.md) for implemented work and remaining gates.
