"""
Étape 5 — Inférence sur le corpus complet
Input  : data_set.json            (dataset original complet)
         model_ner/               (modèle entraîné)
Output : resultats_inference.json (dataset ENRICHI avec les entités détectées)

Le fichier de sortie conserve TOUS les champs originaux + ajoute "entities"
"""

import json
import re
import spacy
from datetime import datetime, timezone

# ── Paramètres ────────────────────────────────────────────────────────────────
INPUT_FILE  = "../data/data_set.json"
MODEL_DIR   = "../data/model_ner"
OUTPUT_FILE = "../data/resultats_inference.json"

# ── Chargement du modèle entraîné ────────────────────────────────────────────
print(f"⏳ Chargement du modèle {MODEL_DIR}...")
nlp = spacy.load(MODEL_DIR)
print("✅ Modèle chargé\n")

# ── Chargement du corpus complet ─────────────────────────────────────────────
print(f"📥 Chargement de {INPUT_FILE}...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

articles = [a for a in data if a.get("text") and len(a["text"].strip()) > 100]
print(f"✅ {len(articles)} articles valides à traiter\n")

# ── Nettoyage du texte ────────────────────────────────────────────────────────
def clean_text(text):
    text = re.sub(r'^[A-Z][A-Z ,\-]+,\s+\w+ \d+\.\s*/TASS/\.\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

# ── Inférence article par article ────────────────────────────────────────────
print("🔍 Extraction des entités en cours...")
resultats = []

for i, article in enumerate(articles):
    # Texte nettoyé pour l'inférence (limité à 1000 chars)
    texte_nettoye = clean_text(article.get("text") or "")[:1000]
    doc = nlp(texte_nettoye)

    # Extraire les entités détectées
    entites = []
    for ent in doc.ents:
        if ent.label_ in {"WEAPON", "MIL_UNIT", "MIL_ORG"}:
            entites.append({
                "entity": ent.text,
                "label":  ent.label_,
                "start":  ent.start_char,
                "end":    ent.end_char
            })

    # ── Garder TOUS les champs originaux + ajouter "entities" ────────────────
    article_enrichi = dict(article)           # copie complète de l'article original
    article_enrichi["text_clean"] = texte_nettoye  # texte nettoyé en bonus
    article_enrichi["entities"]   = entites   # entités détectées ajoutées

    resultats.append(article_enrichi)

    if (i + 1) % 2000 == 0:
        print(f"  ✔ {i+1}/{len(articles)} articles traités...")

print(f"  ✔ {len(articles)}/{len(articles)} articles traités...")

# ── Statistiques ─────────────────────────────────────────────────────────────
articles_avec_entites = [r for r in resultats if r["entities"]]
counts = {"WEAPON": 0, "MIL_UNIT": 0, "MIL_ORG": 0}
for r in resultats:
    for ent in r["entities"]:
        counts[ent["label"]] += 1

print(f"\n📊 Résultats :")
print(f"  Articles traités          : {len(resultats)}")
print(f"  Articles avec entités     : {len(articles_avec_entites)}")
print(f"  Articles sans entité      : {len(resultats) - len(articles_avec_entites)}")
print(f"\n  WEAPON    : {counts['WEAPON']}")
print(f"  MIL_UNIT  : {counts['MIL_UNIT']}")
print(f"  MIL_ORG   : {counts['MIL_ORG']}")
print(f"  TOTAL     : {sum(counts.values())}")

# ── Sauvegarde ────────────────────────────────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(resultats, f, ensure_ascii=False, indent=2)

print(f"\n✅ {OUTPUT_FILE} sauvegardé — dataset complet enrichi avec les labels !")
