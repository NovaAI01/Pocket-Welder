#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = REPO_ROOT / "data" / "observation_drafts"
DEFAULT_OCR_SCRIPT = REPO_ROOT / "scripts" / "ocr_probe.py"
DEFAULT_INSPECT_SCRIPT = REPO_ROOT / "scripts" / "inspect_image.py"


def run_command(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        return (
            f"[command failed]\n"
            f"cmd: {' '.join(cmd)}\n"
            f"stdout:\n{stdout or '[empty]'}\n"
            f"stderr:\n{stderr or '[empty]'}"
        )
    return result.stdout.strip() or "[empty output]"


def build_draft(
    source_image: Path,
    case_id: str,
    raw_ocr_text: str,
    image_notes: str,
) -> str:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return f"""# Manual Observation Draft

## Metadata
- case_id: {case_id}
- source_image: {source_image}
- generated_at_utc: {generated_at}
- status: draft_prefilled_requires_human_review

---

## MACHINE OUTPUT (ASSISTIVE ONLY)

### Raw OCR Payload

```text
{raw_ocr_text}
```

### Image Inspection

```text
{image_notes}
```

---

## HUMAN OBSERVATION (EDIT THIS SECTION ONLY)

### Weld symbol presence
- observed_symbol_type: [unknown]
- confidence_note: [human review required]

### Side / reference line observations
- arrow_side_or_other_side: [unknown]
- reference_line_notes: [unknown]

### Dimensions / counts
- size_mm: [unknown]
- length_mm: [unknown]
- pitch_mm: [unknown]
- weld_count: [unknown]

### Contour / finish
- contour: [unknown]
- finish_method: [unknown]

### Tail / process / notes
- tail_text: [unknown]
- process_notes: [unknown]

### Free observation notes
- [Add direct visual observations here]

---

## HUMAN REVIEW CHECKLIST
- [ ] OCR checked against image
- [ ] inspection notes checked against image
- [ ] symbol interpretation manually verified
- [ ] unknowns resolved where visible
- [ ] assumptions removed
- [ ] ready for extractor formatting
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a semi-automated observation draft from image + assistive OCR."
    )
    parser.add_argument("image_path", help="Path to source image")
    parser.add_argument("--case-id", default=None, help="Optional case identifier")
    parser.add_argument(
        "--ocr-script",
        default=str(DEFAULT_OCR_SCRIPT),
        help="Path to OCR probe script",
    )
    parser.add_argument(
        "--inspect-script",
        default=str(DEFAULT_INSPECT_SCRIPT),
        help="Path to image inspection script",
    )
    args = parser.parse_args()

    image_path = Path(args.image_path).expanduser().resolve()
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    case_id = args.case_id or image_path.stem
    output_path = DRAFT_DIR / f"{case_id}_observation_draft.md"
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)

    ocr_script = Path(args.ocr_script).expanduser().resolve()
    inspect_script = Path(args.inspect_script).expanduser().resolve()

    raw_ocr_text = "[ocr script not found]"
    image_notes = "[inspect script not found]"

    if ocr_script.exists():
        raw_ocr_text = run_command([sys.executable, str(ocr_script), str(image_path)])

    if inspect_script.exists():
        image_notes = run_command([sys.executable, str(inspect_script), str(image_path)])

    draft_text = build_draft(
        source_image=image_path,
        case_id=case_id,
        raw_ocr_text=raw_ocr_text,
        image_notes=image_notes,
    )

    output_path.write_text(draft_text, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
