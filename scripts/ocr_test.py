from pathlib import Path
import sys

from PIL import Image
import pytesseract


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/ocr_test.py <image_path>")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"ERROR: file not found: {image_path}")
        raise SystemExit(1)

    if not image_path.is_file():
        print(f"ERROR: not a file: {image_path}")
        raise SystemExit(1)

    try:
        image = Image.open(image_path)
    except Exception as exc:
        print(f"ERROR: failed to open image: {exc}")
        raise SystemExit(1)

    text = pytesseract.image_to_string(image)

    print("OCR_TEXT_START")
    print(text.strip())
    print("OCR_TEXT_END")


if __name__ == "__main__":
    main()
