"""Collecte des métriques reproductibles du pipeline Military-NER-TASS."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def collect_metrics(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    data_dir = root / "data"
    result_path = data_dir / "resultats_inference.json"
    metrics: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "files": {},
    }
    for name in ["data_set.json", "data_set_nettoyé.json", "annotations_spacy.json", "resultats_inference.json"]:
        p = data_dir / name
        metrics["files"][name] = {"exists": p.exists(), "size_bytes": p.stat().st_size if p.exists() else 0}
    if result_path.exists():
        with result_path.open("r", encoding="utf-8") as f:
            rows = json.load(f)
        counts = {"WEAPON": 0, "MIL_UNIT": 0, "MIL_ORG": 0}
        articles_with_entities = 0
        for row in rows:
            entities = row.get("entities", []) or []
            if entities:
                articles_with_entities += 1
            for ent in entities:
                label = ent.get("label")
                if label in counts:
                    counts[label] += 1
        metrics.update({
            "articles_traitees": len(rows),
            "articles_avec_entites": articles_with_entities,
            "articles_sans_entite": len(rows) - articles_with_entities,
            "entites_par_label": counts,
            "entites_total": sum(counts.values()),
            "resultats_size_bytes": result_path.stat().st_size,
        })
    return metrics


def write_metrics(project_root: str | Path, output: str | Path | None = None) -> Path:
    root = Path(project_root)
    out = Path(output) if output else root / "logs" / "pipeline_metrics.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(collect_metrics(root), f, ensure_ascii=False, indent=2)
    return out
