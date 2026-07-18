"""
Étape 3a — Conversion des annotations au format spaCy (.spacy)
Input  : ../data/annotations_llm.json
Output : ../data/train.spacy  (80%)
         ../data/dev.spacy    (20%)
"""

import json
import random
import spacy
from spacy.tokens import DocBin

# ── Paramètres ────────────────────────────────────────────────────────────────
INPUT_FILE   = "../data/annotations_llm.json"
TRAIN_FILE   = "../data/train.spacy"
DEV_FILE     = "../data/dev.spacy"
TRAIN_RATIO  = 0.8
RANDOM_SEED  = 42

random.seed(RANDOM_SEED)

# ── Chargement ────────────────────────────────────────────────────────────────
print("📥 Chargement des annotations LLM...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

random.shuffle(data)
split = int(len(data) * TRAIN_RATIO)
train_data = data[:split]
dev_data   = data[split:]

print(f"  Train : {len(train_data)} articles")
print(f"  Dev   : {len(dev_data)} articles\n")

# ── Chargement du modèle de base ─────────────────────────────────────────────
nlp = spacy.load("en_core_web_sm")

# ── Conversion en DocBin ──────────────────────────────────────────────────────
def convert(data, output_path):
    db = DocBin()
    skipped = 0
    for text, annot in data:
        doc = nlp.make_doc(text)
        ents = []
        seen = set()
        for start, end, label in annot["entities"]:
            # Éviter les chevauchements
            overlap = any(not (end <= s or start >= e) for s, e in seen)
            if not overlap and start < end <= len(text):
                span = doc.char_span(start, end, label=label)
                if span:
                    ents.append(span)
                    seen.add((start, end))
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)
    print(f"  ✅ {output_path} — {len(data)} docs")

print("⚙️  Conversion en cours...")
convert(train_data, TRAIN_FILE)
convert(dev_data,   DEV_FILE)

print("\n✅ Fichiers .spacy créés !")
print("➡️  Étape suivante : python -m spacy init config config.cfg --lang en --pipeline ner")
