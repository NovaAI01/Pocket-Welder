from pathlib import Path
import json
import sys

from PIL import Image
import pytesseract


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/ocr_probe.py <image_path>")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"ERROR: file not found: {image_path}")
        raise SystemExit(1)

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image).strip()

    result = {
        "image": str(image_path),
        "ocr_text": text,
        "has_text": bool(text)
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
