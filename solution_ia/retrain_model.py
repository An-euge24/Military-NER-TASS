"""Point d'entrée documenté pour le réentraînement contrôlé."""
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAINING_SCRIPT = PROJECT_ROOT / "app" / "step4_training_ner.py"

if __name__ == "__main__":
    if not TRAINING_SCRIPT.exists():
        raise FileNotFoundError(f"Script d'entraînement introuvable : {TRAINING_SCRIPT}")
    print("Réentraînement lancé après validation des nouvelles annotations...")
    raise SystemExit(subprocess.call([sys.executable, str(TRAINING_SCRIPT)], cwd=PROJECT_ROOT))
