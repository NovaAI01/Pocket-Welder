from pathlib import Path
import sys

ROOT = Path.home() / "Dev" / "pocket_welder"
INPUT_DIR = ROOT / "inputs"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/load_drawing.py <filename>")
        raise SystemExit(1)

    filename = sys.argv[1]
    path = INPUT_DIR / filename

    if not path.exists():
        print(f"ERROR: file not found: {path}")
        raise SystemExit(1)

    if not path.is_file():
        print(f"ERROR: not a file: {path}")
        raise SystemExit(1)

    suffix = path.suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".pdf"}:
        print(f"ERROR: unsupported file type: {suffix}")
        raise SystemExit(1)

    print("LOAD OK")
    print(f"path={path}")
    print(f"type={suffix}")
    print(f"size_bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
