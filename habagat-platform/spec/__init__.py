"""Habagat Agent Spec: JSON Schema + Python validation helpers.

Traces to: docs/habagat/architecture/53-api-and-interface-contracts.md §4.1 (normative)
"""
from pathlib import Path
import json
from typing import Any

import jsonschema

SCHEMA_PATH = Path(__file__).parent / "agent_spec.schema.json"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text())


def validate_agent_spec(doc: dict[str, Any]) -> list[str]:
    """Validate a parsed agent.yaml document against the normative schema.

    Returns a list of human-readable error strings (empty = valid). We collect
    ALL errors rather than raising on the first one — Doc 53 §4.1's schema has
    several independent branches (R2/R3 conditionals in $defs.toolReference)
    and a blueprint author should see every violation in one pass, not
    fix-and-recompile once per error.
    """
    schema = load_schema()
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]
