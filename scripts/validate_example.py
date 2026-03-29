import json
from pathlib import Path

try:
    import jsonschema
except ImportError:
    raise SystemExit(
        "Missing dependency: jsonschema\n"
        "Install with: pip install jsonschema"
    )

ROOT = Path.home() / "Dev" / "pocket_welder"
SCHEMA_PATH = ROOT / "schema" / "weld_instruction.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "example_output.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    schema = load_json(SCHEMA_PATH)
    example = load_json(EXAMPLE_PATH)

    jsonschema.validate(instance=example, schema=schema)
    print("VALID: example_output.json matches weld_instruction.schema.json")


if __name__ == "__main__":
    main()
