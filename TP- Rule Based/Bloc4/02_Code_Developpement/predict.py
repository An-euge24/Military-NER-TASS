"""
Fonctions de prédiction du modèle Military-NER-TASS.

Le code fonctionne :
- en local depuis le projet VSCode ;
- dans Docker depuis /app/model_ner.
"""

from pathlib import Path
import os

import spacy


def find_default_model():
    """
    Recherche automatiquement le dossier model_ner.

    Dans Docker :
        /app/model_ner

    En local :
        racine_du_projet/model_ner
    """

    docker_model = Path("/app/model_ner")

    if docker_model.is_dir():
        return docker_model

    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        candidate = parent / "model_ner"

        if candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        "Impossible de trouver le dossier model_ner. "
        "Vérifie que le modèle est présent à la racine du projet."
    )


# La variable d'environnement Docker est prioritaire.
MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        str(find_default_model())
    )
)


_nlp = None


def load_model():
    """
    Charge le modèle spaCy une seule fois.
    """
    global _nlp

    if _nlp is None:
        if not MODEL_PATH.is_dir():
            raise FileNotFoundError(
                f"Modèle introuvable : {MODEL_PATH}"
            )

        print(f"Chargement du modèle depuis : {MODEL_PATH}")
        _nlp = spacy.load(MODEL_PATH)

    return _nlp


def predict_entities(text: str):
    """
    Analyse un texte et retourne les entités détectées.
    """
    if not isinstance(text, str):
        raise ValueError(
            "Le champ text doit être une chaîne de caractères."
        )

    if not text.strip():
        raise ValueError(
            "Le champ text ne peut pas être vide."
        )

    nlp = load_model()
    document = nlp(text)

    entities = []

    for entity in document.ents:
        entities.append(
            {
                "text": entity.text,
                "label": entity.label_,
                "start": entity.start_char,
                "end": entity.end_char,
            }
        )

    return entities