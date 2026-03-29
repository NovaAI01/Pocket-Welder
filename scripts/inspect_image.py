#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image


def describe_image(image_path: Path) -> str:
    with Image.open(image_path) as image:
        width, height = image.size
        mode = image.mode
        image_format = image.format or "unknown"

        grayscale = mode in {"1", "L", "LA"}
        has_alpha = "A" in mode

        return "\n".join(
            [
                f"image_path: {image_path.resolve()}",
                f"file_format: {image_format}",
                f"width_px: {width}",
                f"height_px: {height}",
                f"mode: {mode}",
                f"grayscale: {str(grayscale).lower()}",
                f"has_alpha: {str(has_alpha).lower()}",
                "visible_text_like_regions: unknown",
                "reference_line_visibility: unknown",
                "symbol_cluster_visibility: unknown",
                "general_notes: image loaded successfully; observational output only",
            ]
        )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/inspect_image.py <image_path>")
        return 1

    image_path = Path(sys.argv[1]).expanduser().resolve()

    if not image_path.exists():
        print(f"ERROR: file not found: {image_path}")
        return 1

    print(describe_image(image_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
