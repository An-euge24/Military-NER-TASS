"""Prédiction NER réutilisable par l'API et les scripts de test."""
from pathlib import Path
import os
import spacy

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = Path(os.getenv("MODEL_PATH", PROJECT_ROOT / "model_ner"))

_nlp = None

def load_model():
    global _nlp
    if _nlp is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modèle introuvable : {MODEL_PATH}")
        _nlp = spacy.load(MODEL_PATH)
    return _nlp

def predict_entities(text: str):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Le champ text doit contenir un texte non vide")
    doc = load_model()(text)
    return [
        {
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        }
        for ent in doc.ents
    ]
