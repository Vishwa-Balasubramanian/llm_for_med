# Data contract — version 0.1

## Report manifest

Use UTF-8 JSONL, one object per report. Each record requires patient_id,
report_id, exam_date, source_path, report_type, language, and is_synthetic.
modality and body_region are optional strings or null.

- patient_id: stable pseudonymous identifier, not a person's name.
- report_id: unique within the entire dataset.
- exam_date: YYYY-MM-DD or null. The examination date, not upload or signing date.
- source_path: relative POSIX path inside the manifest folder, ending in .txt or .pdf.
- report_type: descriptive type, e.g. radiology.
- language: language code, e.g. en or de.
- is_synthetic: boolean; false only for actual project data.

See data/examples/reports.jsonl for complete records.
Missing examination dates are flagged and excluded from dated timeline analysis.
Different files on the same date do not establish longitudinal follow-up.
PDF intake validation only checks file presence and header; parsing/OCR is Phase 2.

## Annotation contract

Each event requires the fields defined in clinical_events/schemas/event.py.
Each event is a mention in a particular report. A finding_id groups mentions of
the same finding and must never connect different patients.

Evidence offsets are zero-based Unicode character indices with an exclusive end,
against Python UTF-8-sig read_text output (universal newlines normalized to LF).
For this phase, exact evidence validation supports TXT only.
PDF page coordinates and canonical extracted text are Phase 2 additions.

The current schema stores one contiguous evidence span per mention.
Cross-report inference must remain unannotated as a reported change unless the
current report explicitly states it. A future temporal-link schema will preserve
both reports' evidence. Event dates, measurements, and multiple evidence spans are
planned extensions before those features are implemented.

Allowed categories, assertion labels, temporal contexts, changes, and device
actions live in event.py. Null anatomy and unknown laterality preserve ambiguity.
Synthetic examples are draft labels, not expert ground truth.

