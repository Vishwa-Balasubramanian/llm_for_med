# Annotation guidelines — draft for expert review

## Scope

Annotate explicit mentions in these three categories:
1. tumor_metastasis: tumor and metastatic findings, including specified lymph nodes.
2. complication: initially thrombosis, ureteral compression, hydronephrosis, fracture.
3. procedure_device: initially ureteral stents, catheters, and explicitly stated procedures.

This initial list comes from the project slides. Reconcile it with the project's
bonus-material event list and an expert before freezing the scope.

## Rules

- Annotate the shortest complete passage that preserves the finding's meaning,
  including relevant negation, uncertainty, side, and change language.
- Keep absence and uncertainty explicit. "No hydronephrosis" is absent, not present.
- "Possible metastasis" is uncertain. Do not upgrade it to confirmed.
- "Old fracture" is historical; the report date is not the fracture onset date.
- "Stent remains in place" means device present; it does not establish insertion.
- Distinguish a planned procedure from one already performed.
- reported_change describes the report's explicit wording, not an inferred diagnosis.
- Use not_stated when change is not described.
- Missing mention in a later report does not mean resolved.
- Stable disease in one location does not make every lesion stable.
- Reuse a finding_id only when anatomy, side, and context support identity.
- When matching is uncertain, use separate finding IDs and record adjudication notes.
- Do not infer a causal link between cancer and a complication from co-occurrence.

## Review procedure

1. Start with a small patient-level development pilot.
2. Two reviewers independently annotate an overlapping subset if available.
3. Resolve disagreements with a qualified clinical reviewer.
4. Record reviewer IDs, annotation version, and decisions in an external review log.
5. Mark expert_reviewed only after review; otherwise keep draft.
6. Freeze the guidelines before annotating the final held-out test set.

The supplied example annotations are hand-authored synthetic demonstrations and
have not undergone clinical expert review.

