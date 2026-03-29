import json
import sys
from pathlib import Path

from extract_from_case import build_output, load_json

ROOT = Path.home() / "Dev" / "pocket_welder"
CASES_DIR = ROOT / "cases"
INPUTS_DIR = ROOT / "inputs"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/run_case.py <case_id>")
        raise SystemExit(1)

    case_id = sys.argv[1]
    case_path = CASES_DIR / case_id / "case.json"

    if not case_path.exists():
        print(f"ERROR: case not found: {case_path}")
        raise SystemExit(1)

    case_data = load_json(case_path)

    image_path = INPUTS_DIR / case_data["source_file"]
    if not image_path.exists():
        print(f"ERROR: source image not found: {image_path}")
        raise SystemExit(1)

    generated_output = build_output(case_data)

    result = {
        "case_id": case_id,
        "image_found": True,
        "image_path": str(image_path),
        "expected_output": case_data["expected_output"],
        "generated_output": generated_output,
        "match": generated_output == case_data["expected_output"]
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
