import json
import sys
from pathlib import Path

ROOT = Path.home() / "Dev" / "pocket_welder"
CASES_DIR = ROOT / "cases"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/show_case.py <case_id>")
        raise SystemExit(1)

    case_id = sys.argv[1]
    case_path = CASES_DIR / case_id / "case.json"

    if not case_path.exists():
        print(f"ERROR: case not found: {case_path}")
        raise SystemExit(1)

    with case_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
