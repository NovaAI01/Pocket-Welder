#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "data" / "corrected_observations"


def extract_section(markdown_text: str, start_heading: str, end_heading: str) -> str:
    start = markdown_text.find(start_heading)
    if start == -1:
        raise ValueError(f"Missing section start: {start_heading}")

    end = markdown_text.find(end_heading, start)
    if end == -1:
        raise ValueError(f"Missing section end: {end_heading}")

    return markdown_text[start + len(start_heading):end].strip()


def extract_metadata(markdown_text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    match = re.search(r"## Metadata\n(.*?)(?:\n---)", markdown_text, re.DOTALL)
    if not match:
        raise ValueError("Could not find Metadata section.")

    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        if ": " not in line:
            continue

        key, value = line[2:].split(": ", 1)
        metadata[key.strip()] = value.strip()

    return metadata


def parse_human_observation(section_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    current_section = None
    free_notes: list[str] = []

    for raw_line in section_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("### "):
            current_section = line[4:].strip().lower()
            continue

        if not line.startswith("- "):
            continue

        content = line[2:].strip()

        if current_section == "free observation notes":
            if content:
                free_notes.append(content)
            continue

        if ": " not in content:
            continue

        key, value = content.split(": ", 1)
        parsed[key.strip()] = value.strip()

    if free_notes:
        parsed["free_observation_notes"] = " ".join(free_notes)

    return parsed


def normalize_unknown(value: str | None):
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned in {"[unknown]", "unknown", "", "[none]", "none"}:
        return None
    return cleaned


def to_number_or_none(value: str | None):
    normalized = normalize_unknown(value)
    if normalized is None:
        return None
    try:
        if "." in normalized:
            return float(normalized)
        return int(normalized)
    except ValueError:
        return normalized


def map_to_human_observation(parsed: dict[str, str]) -> dict:
    return {
        "visible_text": None,
        "symbol_guess": normalize_unknown(parsed.get("observed_symbol_type")),
        "side_guess": normalize_unknown(parsed.get("arrow_side_or_other_side")),
        "contour_guess": normalize_unknown(parsed.get("contour")),
        "size_mm": to_number_or_none(parsed.get("size_mm")),
        "length_mm": to_number_or_none(parsed.get("length_mm")),
        "pitch_mm": to_number_or_none(parsed.get("pitch_mm")),
        "count": to_number_or_none(parsed.get("weld_count")),
        "visible_symbol_components": [],
    }


def collect_adapter_notes(parsed: dict[str, str]) -> list[str]:
    notes: list[str] = []

    if normalize_unknown(parsed.get("confidence_note")) is not None:
        notes.append(f"confidence_note: {parsed['confidence_note']}")

    if normalize_unknown(parsed.get("reference_line_notes")) is not None:
        notes.append(f"reference_line_notes: {parsed['reference_line_notes']}")

    if normalize_unknown(parsed.get("finish_method")) is not None:
        notes.append(f"finish_method: {parsed['finish_method']}")

    if normalize_unknown(parsed.get("tail_text")) is not None:
        notes.append(f"tail_text: {parsed['tail_text']}")

    if normalize_unknown(parsed.get("process_notes")) is not None:
        notes.append(f"process_notes: {parsed['process_notes']}")

    if normalize_unknown(parsed.get("free_observation_notes")) is not None:
        notes.append(f"free_observation_notes: {parsed['free_observation_notes']}")

    return notes


def build_output(draft_path: Path, metadata: dict[str, str], parsed: dict[str, str]) -> dict:
    return {
        "source_draft": str(draft_path.resolve()),
        "adapter_version": "v0.1",
        "case_id": metadata.get("case_id"),
        "source_image": metadata.get("source_image"),
        "human_observation": map_to_human_observation(parsed),
        "adapter_notes": collect_adapter_notes(parsed),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a corrected observation draft into current human_observation-shaped JSON."
    )
    parser.add_argument("draft_path", help="Path to corrected observation markdown draft")
    parser.add_argument("--output", default=None, help="Optional explicit output JSON path")
    args = parser.parse_args()

    draft_path = Path(args.draft_path).expanduser().resolve()
    if not draft_path.exists():
        raise FileNotFoundError(f"Draft file not found: {draft_path}")

    markdown_text = draft_path.read_text(encoding="utf-8")
    metadata = extract_metadata(markdown_text)
    human_section = extract_section(
        markdown_text,
        "## HUMAN OBSERVATION (EDIT THIS SECTION ONLY)",
        "## HUMAN REVIEW CHECKLIST",
    )
    parsed = parse_human_observation(human_section)
    output_payload = build_output(draft_path, metadata, parsed)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = OUTPUT_DIR / f"{draft_path.stem}.json"

    output_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
