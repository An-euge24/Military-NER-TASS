"""
Étape 2 — Extraction du texte
Input  : data_set.json      (21 742 articles TASS bruts)
Output : data_set_nettoyé.json (liste de 800 textes nettoyés, tirés aléatoirement)
"""

import json
import re
import random
import time
from pathlib import Path

# ── Paramètres ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'data_set.json'
OUTPUT_FILE = BASE_DIR / 'data' / 'data_set_nettoyé.json'
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
NB_ARTICLES = 800
RANDOM_SEED = 42          # changer pour un tirage différent

# ── Chargement ────────────────────────────────────────────────────────────────
start = time.perf_counter()
with INPUT_FILE.open('r', encoding='utf-8') as f:
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

duration = time.perf_counter() - start
metrics = {'input_articles': len(data), 'valid_articles': len(articles_valides), 'sample_articles': len(corpus), 'duration_seconds': round(duration, 2), 'output_size_bytes': OUTPUT_FILE.stat().st_size}
with (LOG_DIR / 'step2_metrics.json').open('w', encoding='utf-8') as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)
print(f"✅ {OUTPUT_FILE} créé — {len(corpus)} textes")
print(f"⏱️ Durée totale : {duration:.2f} s | taille sortie : {OUTPUT_FILE.stat().st_size} octets")
