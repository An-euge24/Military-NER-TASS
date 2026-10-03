"""
Étape 4 — Fine-tuning du modèle NER spaCy
Input  : annotations_spacy.json   (516 articles annotés)
Output : model_ner/               (modèle entraîné)

Prérequis : pip install spacy
            python -m spacy download en_core_web_sm
"""

import json
import random
import time
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ── Paramètres ────────────────────────────────────────────────────────────────
INPUT_FILE   = DATA_DIR / "annotations_spacy.json"
OUTPUT_DIR   = BASE_DIR / "model_ner"
N_ITER       = 30        # nombre d'époques d'entraînement
TRAIN_RATIO  = 0.8       # 80% entraînement / 20% validation
RANDOM_SEED  = 42

random.seed(RANDOM_SEED)

# ── Chargement des annotations ────────────────────────────────────────────────
start_total = time.perf_counter()
model_start = time.perf_counter()
print("📥 Chargement des annotations...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Mélanger les données
random.shuffle(data)

# Découpage train / validation
split = int(len(data) * TRAIN_RATIO)
train_data = data[:split]
val_data   = data[split:]

print(f"  Train : {len(train_data)} articles")
print(f"  Valid : {len(val_data)} articles\n")

# ── Chargement du modèle de base ─────────────────────────────────────────────
print("⏳ Chargement du modèle de base en_core_web_sm...")
nlp = spacy.load("en_core_web_sm")
print(f"✅ Modèle de base chargé en {time.perf_counter() - model_start:.2f} s")

# Ajouter le composant NER s'il n'existe pas
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Ajouter nos labels personnalisés
for label in ["WEAPON", "MIL_UNIT", "MIL_ORG"]:
    ner.add_label(label)

# ── Préparation des exemples d'entraînement ───────────────────────────────────
def make_examples(nlp, data):
    examples = []
    for text, annotations in data:
        doc = nlp.make_doc(text)
        # Filtrer les entités qui se chevauchent
        spans = []
        seen = set()
        for start, end, label in annotations["entities"]:
            overlap = False
            for s, e in seen:
                if not (end <= s or start >= e):
                    overlap = True
                    break
            if not overlap:
                spans.append((start, end, label))
                seen.add((start, end))
        example = Example.from_dict(doc, {"entities": spans})
        examples.append(example)
    return examples

# ── Entraînement ──────────────────────────────────────────────────────────────
print("🧠 Début de l'entraînement...\n")

# Désactiver les pipes non nécessaires pendant l'entraînement
other_pipes = [p for p in nlp.pipe_names if p != "ner"]

with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()

    for iteration in range(N_ITER):
        random.shuffle(train_data)
        losses = {}
        examples = make_examples(nlp, train_data)

        # Mini-batches
        batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            nlp.update(batch, drop=0.3, losses=losses)

        # Afficher la progression
        if (iteration + 1) % 5 == 0:
            print(f"  Époque {iteration+1:2d}/{N_ITER} — Loss NER : {losses['ner']:.2f}")

# ── Évaluation sur le jeu de validation ──────────────────────────────────────
print("\n📊 Évaluation sur le jeu de validation...")
val_examples = make_examples(nlp, val_data)
scores = nlp.evaluate(val_examples)

ner_scores = scores.get("ents_p", 0), scores.get("ents_r", 0), scores.get("ents_f", 0)
print(f"  Précision  (P) : {ner_scores[0]:.2%}")
print(f"  Rappel     (R) : {ner_scores[1]:.2%}")
print(f"  F1-score       : {ner_scores[2]:.2%}")

# ── Sauvegarde du modèle ──────────────────────────────────────────────────────
output_path = Path(OUTPUT_DIR)
output_path.mkdir(exist_ok=True)
nlp.to_disk(output_path)

print(f"\n✅ Modèle sauvegardé dans : {OUTPUT_DIR}/")
duration = time.perf_counter() - start_total
metrics = {"train_articles": len(train_data), "validation_articles": len(val_data), "iterations": N_ITER, "precision": ner_scores[0], "recall": ner_scores[1], "f1": ner_scores[2], "duration_seconds": round(duration, 2), "model_dir": str(output_path)}
with (LOG_DIR / "step4_metrics.json").open("w", encoding="utf-8") as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)
print(f"⏱️ Durée totale entraînement + évaluation : {duration:.2f} s")
print(f"📊 Métriques sauvegardées dans : {LOG_DIR / 'step4_metrics.json'}")
print("🎯 Prêt pour l'étape 5 — Inférence sur le corpus complet !")
