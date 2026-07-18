"""
Étape 2 — Extraction du texte
Input  : data_set.json      (21 742 articles TASS bruts)
Output : data_set_nettoyé.json (liste de 800 textes nettoyés, tirés aléatoirement)
"""

import json
import re
import random

# ── Paramètres ────────────────────────────────────────────────────────────────
INPUT_FILE  = '../data/data_set.json'
OUTPUT_FILE = '../data/data_set_nettoyé.json'
NB_ARTICLES = 800
RANDOM_SEED = 42          # changer pour un tirage différent

# ── Chargement ────────────────────────────────────────────────────────────────
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ── Filtrage : articles avec texte valide ────────────────────────────────────
articles_valides = [a for a in data if a.get('text') and len(a['text'].strip()) > 100]
print(f"Articles valides : {len(articles_valides)}")

# ── Tirage aléatoire ─────────────────────────────────────────────────────────
random.seed(RANDOM_SEED)
sample = random.sample(articles_valides, NB_ARTICLES)

# ── Nettoyage ────────────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Nettoie un texte d'article TASS."""
    # Supprimer l'en-tête agence : "MOSCOW, March 11. /TASS/."
    text = re.sub(r'^[A-Z][A-Z ,\-]+,\s+\w+ \d+\.\s*/TASS/\.\s*', '', text)
    # Espaces multiples → un seul espace
    text = re.sub(r'\s+', ' ', text)
    # Caractères de contrôle parasites
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

# ── Extraction du texte uniquement ───────────────────────────────────────────
corpus = [clean_text(a['text']) for a in sample]

# ── Sauvegarde ────────────────────────────────────────────────────────────────
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, ensure_ascii=False, indent=2)

print(f"✅ {OUTPUT_FILE} créé — {len(corpus)} textes")
