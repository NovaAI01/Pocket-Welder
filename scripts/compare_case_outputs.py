import json
import sys
from pathlib import Path
from extract_from_case import build_output, load_json

ROOT = Path.home() / "Dev" / "pocket_welder"
CASES_DIR = ROOT / "cases"
INPUTS_DIR = ROOT / "inputs"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_manual_output(case_data: dict) -> dict:
    obs = case_data["human_observation"]

    weld = {
        "joint_id": "J1",
        "process": None,
        "symbol": obs.get("symbol_guess"),
        "side": obs.get("side_guess"),
        "contour": obs.get("contour_guess"),
        "size_mm": obs.get("size_mm"),
        "length_mm": obs.get("length_mm"),
        "pitch_mm": obs.get("pitch_mm"),
        "finish": None,
        "count": obs.get("count"),
        "reference_text": obs.get("visible_text"),
        "confidence": 0.78,
        "notes": [
            "Arrow indicates other side",
            "Visible symbol appears to contain multiple components",
            "Component 1 resembles square groove",
            "Component 2 resembles single bevel groove",
            "Single flat symbol field is insufficient for exact representation",
            "No explicit size shown",
            "No explicit length or pitch shown"
        ]
    }

    return {
        "drawing_id": case_data["drawing_id"],
        "source_file": case_data["source_file"],
        "notes": [
            "Manual extraction from real drawing",
            "Reference text preserved without interpretation",
            "Compound weld symbol observed: square groove plus single bevel groove"
        ],
        "welds": [weld]
    }
def diff_values(expected, actual, path="root"):
    diffs = []

    if type(expected) != type(actual):
        diffs.append({
            "path": path,
            "expected": expected,
            "actual": actual,
            "reason": f"type_mismatch: {type(expected).__name__} != {type(actual).__name__}"
        })
        return diffs

    if isinstance(expected, dict):
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())

        for key in sorted(expected_keys - actual_keys):
            diffs.append({
                "path": f"{path}.{key}",
                "expected": expected[key],
                "actual": "__missing__",
                "reason": "missing_in_actual"
            })

        for key in sorted(actual_keys - expected_keys):
            diffs.append({
                "path": f"{path}.{key}",
                "expected": "__missing__",
                "actual": actual[key],
                "reason": "extra_in_actual"
            })

        for key in sorted(expected_keys & actual_keys):
            diffs.extend(diff_values(expected[key], actual[key], f"{path}.{key}"))

        return diffs

    if isinstance(expected, list):
        if len(expected) != len(actual):
            diffs.append({
                "path": path,
                "expected": f"length={len(expected)}",
                "actual": f"length={len(actual)}",
                "reason": "list_length_mismatch"
            })

        for i, (e_item, a_item) in enumerate(zip(expected, actual)):
            diffs.extend(diff_values(e_item, a_item, f"{path}[{i}]"))

        return diffs

    if expected != actual:
        diffs.append({
            "path": path,
            "expected": expected,
            "actual": actual,
            "reason": "value_mismatch"
        })

    return diffs


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/compare_case_outputs.py <case_id>")
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

    expected_output = case_data["expected_output"]
    generated_output = build_output(case_data)
    diffs = diff_values(expected_output, generated_output)

    result = {
        "case_id": case_id,
        "image_path": str(image_path),
        "match": len(diffs) == 0,
        "diff_count": len(diffs),
        "diffs": diffs
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
