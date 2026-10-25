"""Read one JSON object per line with useful error locations."""

import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8-sig") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path.name}:{line_number}: expected a JSON object")
            records.append(record)
    return records

