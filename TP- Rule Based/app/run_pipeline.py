"""Orchestrateur optionnel du pipeline avec logs horodatés.

À lancer depuis la racine du projet. Les scripts existants restent inchangés.
Le script ne relance pas l'entraînement par défaut, afin d'éviter un traitement
long non nécessaire pour une démonstration.
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from pipeline_metrics import write_metrics

STEPS = {
    "step2": ["app/step2_extraction.py"],
    "step3": ["app/step3_annotation_rulebased.py"],
    "step4": ["app/step4_training_ner.py"],
    "step5": ["app/step5_inference.py"],
    "step6a": ["step6a_ingestion_elasticsearch_local.py"],
}
ORDER = list(STEPS)

def run_step(root: Path, name: str, log) -> int:
    command = [sys.executable, *STEPS[name]]
    start = time.perf_counter()
    stamp = datetime.now().isoformat(timespec="seconds")
    log.write(f"\n[{stamp}] START {name}: {' '.join(command)}\n")
    log.flush()
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log.write(result.stdout)
    elapsed = time.perf_counter() - start
    log.write(f"[{datetime.now().isoformat(timespec='seconds')}] END {name} | return_code={result.returncode} | duration_s={elapsed:.2f}\n")
    log.flush()
    return result.returncode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-step", choices=ORDER, default="step2")
    parser.add_argument("--to-step", choices=ORDER, default="step6a")
    parser.add_argument("--skip-training", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    logs = root / "logs"; logs.mkdir(exist_ok=True)
    log_path = logs / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    start = time.perf_counter()
    first = ORDER.index(args.from_step); last = ORDER.index(args.to_step)
    if first > last:
        raise SystemExit("--from-step doit être antérieur ou égal à --to-step")
    selected = ORDER[first:last+1]
    if args.skip_training and "step4" in selected:
        selected.remove("step4")
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"PIPELINE_START={datetime.now().isoformat()}\n")
        log.write(f"PROJECT_ROOT={root}\nSTEPS={','.join(selected)}\n")
        for name in selected:
            code = run_step(root, name, log)
            if code != 0:
                log.write(f"PIPELINE_STOPPED_ON={name}\n")
                raise SystemExit(code)
        elapsed = time.perf_counter() - start
        log.write(f"PIPELINE_END={datetime.now().isoformat()}\nTOTAL_DURATION_S={elapsed:.2f}\n")
    metrics_path = write_metrics(root, logs / "pipeline_metrics.json")
    print(f"Log créé : {log_path}")
    print(f"Métriques créées : {metrics_path}")

if __name__ == "__main__":
    main()
