"""Usage: python -m clinical_events.cli.validate_dataset MANIFEST [--annotations FILE]."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from clinical_events.data.load_reports import load_reports
from clinical_events.data.validate_reports import validate_reports
from clinical_events.data.validate_annotations import validate_annotations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--annotations", type=Path)
    args = parser.parse_args()
    try:
        reports = load_reports(args.manifest)
        result = validate_reports(reports, args.manifest.parent)
        if args.annotations:
            annotations = validate_annotations(args.annotations, reports, args.manifest.parent)
            result.errors.extend(annotations.errors)
            result.warnings.extend(annotations.warnings)
            result.summary.update(annotations.summary)
        print(json.dumps(asdict(result), indent=2))
        return 1 if result.errors else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"errors": [str(exc)]}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

