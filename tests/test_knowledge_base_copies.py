"""The knowledge base exists twice: knowledge_base/ (project root, dev) and
src/med_vehicle_intelligence/knowledge_base/ (package data -- what the server actually loads).
2026-09-23: a keyword edit landed in the root copy only and every new test failed, because the
loader prefers the package copy. Any file present in both places must be byte-identical."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEV = ROOT / "knowledge_base"
PKG = ROOT / "src" / "med_vehicle_intelligence" / "knowledge_base"


def test_shared_knowledge_files_are_identical():
    shared = sorted(p.name for p in PKG.glob("*.json") if (DEV / p.name).exists())
    assert shared, "no shared knowledge files found -- the check would pass vacuously"
    differ = [n for n in shared if (DEV / n).read_bytes() != (PKG / n).read_bytes()]
    assert not differ, f"knowledge_base copies differ: {differ} -- edit both, or the server ignores yours"
