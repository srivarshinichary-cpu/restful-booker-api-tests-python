"""JSON schema validation helper."""
import json
from pathlib import Path

from jsonschema import validate

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(name: str) -> dict:
    with open(SCHEMA_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def assert_matches_schema(instance: dict, schema_name: str) -> None:
    validate(instance=instance, schema=load_schema(schema_name))
