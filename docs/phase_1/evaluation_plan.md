# Evaluation plan

## Main question

Does selective historical retrieval plus evidence verification improve event
extraction and temporal linking over a fixed pipeline?

## Data partitions

Partition by patient, never by report. Use development patients for prompts,
annotation-rule revisions, and model selection. Keep test patients untouched until
the final experiment. Train is reserved for future training or example selection;
no model training is required in Phase 1.

The split utility makes approximately 60/20/20 train/dev/test groups with a fixed
seed, at least one patient per group, and a manifest fingerprint.
Three synthetic patients only demonstrate isolation, not valid sample size.
Freeze the resulting file; patient additions can change a recomputed split.
Before freezing real data, inspect cancer-type, modality, language, and follow-up
coverage in each partition and version any clinically justified adjustment.

## Experiments planned for later phases

A. Structured extraction only.
B. Extraction plus deterministic validation.
C. Fixed retrieval plus semantic verification.
D. Adaptive retrieval plus semantic verification.

Keep base model, dataset, and output contract comparable. Record model version,
prompt version, retrieval settings, correction budget, token usage, and run time.
Evaluate with matched resource limits where feasible and report actual costs.

## Metrics and reference labels

- Event precision/recall/F1 by category, with a documented mention-matching rule.
- Assertion, temporal context, and reported-change accuracy on matched events.
- Finding-link precision/recall against expert-reviewed links.
- Citation support and coverage: exact text matching alone is insufficient.
- Verifier false acceptance/rejection against expert correctness judgments.
- Review rate and coverage of automatically accepted results.
- Repeated-run correctness; consistency alone is not correctness.
- Median and tail latency, token usage, and processing cost.
- Patient-level bootstrap intervals when the real sample supports them.

Report source/OCR errors separately from extraction and reasoning errors.
Predefine matching tolerances and success criteria after the development pilot,
before opening the test set. Do not invent accuracy thresholds in advance of data.
Expert annotations, not an LLM judge alone, are the evaluation reference.

