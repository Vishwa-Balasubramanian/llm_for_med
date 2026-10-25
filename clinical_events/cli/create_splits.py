"""Usage: python -m clinical_events.cli.create_splits MANIFEST --output FILE."""

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from clinical_events.data.load_reports import load_reports
from clinical_events.data.split_patients import split_patients
from clinical_events.data.validate_reports import validate_reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    try:
        reports = load_reports(args.manifest)
        validation = validate_reports(reports, args.manifest.parent)
        if validation.errors:
            print(json.dumps(asdict(validation), indent=2))
            return 1
        payload = {
            "seed": args.seed,
            "manifest_sha256": sha256(args.manifest.read_bytes()).hexdigest(),
            "patient_splits": split_patients(reports, args.seed),
            "note": "Freeze this file. Adding patients requires an explicitly versioned split.",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents accidentally replacing a frozen test split.
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2)
            stream.write("\n")
        print(f"Created {args.output}")
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"errors": [str(exc)]}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

