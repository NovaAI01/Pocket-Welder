import json
from pathlib import Path

from extract_from_case import build_output, load_json

ROOT = Path.home() / "Dev" / "pocket_welder"
CASES_DIR = ROOT / "cases"
INPUTS_DIR = ROOT / "inputs"


def main():
    case_dirs = sorted([p for p in CASES_DIR.iterdir() if p.is_dir()])

    if not case_dirs:
        print("No case directories found.")
        raise SystemExit(1)

    results = []
    passed = 0
    failed = 0

    for case_dir in case_dirs:
        case_path = case_dir / "case.json"

        if not case_path.exists():
            results.append({
                "case_id": case_dir.name,
                "status": "error",
                "reason": "missing case.json"
            })
            failed += 1
            continue

        case_data = load_json(case_path)
        image_path = INPUTS_DIR / case_data["source_file"]

        if not image_path.exists():
            results.append({
                "case_id": case_data.get("case_id", case_dir.name),
                "status": "error",
                "reason": f"missing source image: {image_path}"
            })
            failed += 1
            continue

        generated_output = build_output(case_data)
        expected_output = case_data["expected_output"]
        match = generated_output == expected_output

        results.append({
            "case_id": case_data["case_id"],
            "source_file": case_data["source_file"],
            "match": match
        })

        if match:
            passed += 1
        else:
            failed += 1

    summary = {
        "total_cases": len(results),
        "passed": passed,
        "failed": failed,
        "results": results
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
