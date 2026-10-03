"""Tests de fumée du projet Military-NER-TASS.

Ces tests ne lancent pas l'inférence complète. Ils vérifient seulement
que les artefacts indispensables sont présents avant un lancement.
"""

from pathlib import Path

# Le dossier racine est le parent du dossier tests.
ROOT = Path(__file__).resolve().parents[1]


def test_project_artifacts_exist():
    """Vérifie que les dossiers principaux du projet existent."""
    assert (ROOT / "app").exists()
    assert (ROOT / "data").exists()
    assert (ROOT / "model_ner").exists()


def test_required_model_metadata_exists():
    """Vérifie que le modèle spaCy contient ses métadonnées."""
    assert (ROOT / "model_ner" / "meta.json").exists()
