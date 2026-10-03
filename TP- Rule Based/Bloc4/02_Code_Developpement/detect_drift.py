"""Détection simple de dérive sur la distribution des catégories."""
import json
import sys
from collections import Counter
from pathlib import Path

LABELS = ("WEAPON", "MIL_UNIT", "MIL_ORG")

def load_results(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def count_labels(items):
    counts = Counter()
    for item in items:
        entities = item.get("entities", []) if isinstance(item, dict) else []
        for entity in entities:
            label = entity.get("label") if isinstance(entity, dict) else None
            if label in LABELS:
                counts[label] += 1
    return counts

def distribution(counts):
    total = sum(counts.values()) or 1
    return {label: counts[label] / total for label in LABELS}

def compare(reference_path, current_path, threshold=0.15):
    ref = distribution(count_labels(load_results(reference_path)))
    cur = distribution(count_labels(load_results(current_path)))
    differences = {label: round(cur[label] - ref[label], 4) for label in LABELS}
    drift = any(abs(value) >= threshold for value in differences.values())
    return {"reference": ref, "current": cur, "differences": differences, "drift_detected": drift, "threshold": threshold}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python detect_drift.py reference.json current.json")
    result = compare(Path(sys.argv[1]), Path(sys.argv[2]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
