# Dataset layout

- examples/: committed, fully synthetic text and draft annotations.
- templates/: empty intake manifest and acquisition checklist.
- private/: place authorized project reports here when available (Git-ignored).
- processed/: generated text and derived records (Git-ignored).
- splits/: frozen patient split files (Git-ignored because they may contain identifiers).

A dataset folder contains a reports.jsonl manifest and a reports/ subfolder.
Source paths are relative to the manifest's parent folder and use forward slashes.

The project-provided de-identified reports are the selected source, but are not
available yet. No real reports have been downloaded or processed.

The validator checks structure, source existence, dates, and evidence references.
It does not establish de-identification, clinical correctness, or dataset access rights.

