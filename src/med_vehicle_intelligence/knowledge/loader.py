"""Knowledge base loader. Reads JSON files once at import and caches."""

import json
from pathlib import Path

# Knowledge base is bundled inside the package as package data.
# Falls back to the project root for local dev if not found.
_PKG_KB = Path(__file__).resolve().parent.parent / "knowledge_base"
_DEV_KB = Path(__file__).resolve().parent.parent.parent.parent / "knowledge_base"
KB_DIR = _PKG_KB if _PKG_KB.exists() else _DEV_KB


def _load(filename: str) -> dict:
    with open(KB_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


REPAIR_COSTS = _load("repair_costs.json")
MAINTENANCE = _load("maintenance_schedules.json")
VEHICLE_ISSUES = _load("vehicle_issues.json")
RED_FLAGS = _load("red_flags.json")
SHOP_QUESTIONS = _load("shop_questions.json")
