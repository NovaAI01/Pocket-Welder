import json
import sys
from pathlib import Path

ROOT = Path.home() / "Dev" / "pocket_welder"
CASES_DIR = ROOT / "cases"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_notes(obs: dict) -> list[str]:
    notes = []

    side = obs.get("side_guess")
    if side == "other_side":
        notes.append("Arrow indicates other side")
    elif side == "arrow_side":
        notes.append("Arrow indicates arrow side")
    elif side == "both_sides":
        notes.append("Callout indicates both sides")

    components = obs.get("visible_symbol_components", [])

    if len(components) == 1:
        guess = components[0].get("guess")
        if guess == "fillet":
            notes.append("Single fillet weld symbol identified")
        else:
            pretty = guess.replace("_", " ") if guess else "symbol"
            notes.append(f"Single {pretty} weld symbol identified")

    elif len(components) > 1:
        notes.append("Visible symbol appears to contain multiple components")
        for idx, component in enumerate(components, start=1):
            guess = component.get("guess")
            if guess:
                pretty = guess.replace("_", " ")
                notes.append(f"Component {idx} resembles {pretty}")
        notes.append("Single flat symbol field is insufficient for exact representation")

    text = obs.get("visible_text") or ""
    if "stitch" in text.lower():
        notes.append("Stitch indicates intermittent weld")

    if obs.get("all_around"):
        notes.append("All-around weld indicated")

    contour = obs.get("contour_guess")
    if contour == "flush_one_side":
        notes.append("Flush required on one side")
    elif contour == "flush":
        notes.append("Flush contour specified")

    if obs.get("size_mm") is None:
        notes.append("No explicit size shown")

    if obs.get("length_mm") is None and obs.get("pitch_mm") is None:
        notes.append("No explicit length or pitch shown")

    return notes


def build_top_notes(obs: dict) -> list[str]:
    notes = [
        "Manual extraction from real drawing",
        "Reference text preserved without interpretation"
    ]

    components = obs.get("visible_symbol_components", [])

    if len(components) == 1:
        guess = components[0].get("guess")
        if guess == "fillet":
            notes.append("Single fillet weld symbol observed")
        elif guess:
            pretty = guess.replace("_", " ")
            notes.append(f"Single {pretty} weld symbol observed")

    elif len(components) > 1:
        component_names = []
        for c in components:
            guess = c.get("guess")
            if guess:
                component_names.append(guess.replace("_", " "))
        if component_names:
            notes.append(
                "Compound weld symbol observed: " + " plus ".join(component_names)
            )

    return notes


def derive_symbol(obs: dict):
    components = obs.get("visible_symbol_components", [])
    if len(components) == 1:
        return components[0].get("guess")
    return obs.get("symbol_guess")


def build_output(case_data: dict) -> dict:
    obs = case_data["human_observation"]

    weld = {
        "joint_id": "J1",
        "process": None,
        "symbol": derive_symbol(obs),
        "side": obs.get("side_guess"),
        "contour": obs.get("contour_guess"),
        "size_mm": obs.get("size_mm"),
        "length_mm": obs.get("length_mm"),
        "pitch_mm": obs.get("pitch_mm"),
        "finish": None,
        "count": obs.get("count"),
        "reference_text": obs.get("visible_text"),
        "confidence": 0.78,
        "notes": build_notes(obs)
    }

    return {
        "drawing_id": case_data["drawing_id"],
        "source_file": case_data["source_file"],
        "notes": build_top_notes(obs),
        "welds": [weld]
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/extract_from_case.py <case_id>")
        raise SystemExit(1)

    case_id = sys.argv[1]
    case_path = CASES_DIR / case_id / "case.json"

    if not case_path.exists():
        print(f"ERROR: case not found: {case_path}")
        raise SystemExit(1)

    case_data = load_json(case_path)
    output = build_output(case_data)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
