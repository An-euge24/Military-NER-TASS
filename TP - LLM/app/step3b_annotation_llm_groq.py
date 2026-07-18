"""
Étape 3b — Annotation avec LLM (Groq API - Llama-3.1)
Input  : ../data/data_set_nettoyé.json
Output : ../data/annotations_llm.json
"""

import json                     
import re                      #permet de manipuler des chaînes de caractères avec des expressions régulières
import time
from groq import Groq          #bibliothèque pour interagir avec l'API Groq (Llama-3.1)        
from datetime import timedelta # calculer la durée totale et moyenne de l'annotation
from dotenv import load_dotenv #  charger les variables d'environnement depuis un fichier .env
import os                      #permet d'accéder aux variables d'environnement et de gérer les chemins de fichiers


# ── ⚠️ METS TA CLÉ GROQ ICI ─────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# ─────────────────────────────────────────────────────────────────────────────

INPUT_FILE   = "../data/data_set_nettoyé.json"
OUTPUT_FILE  = "../data/annotations_llm.json"
MAX_ARTICLES = 500

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a military NER expert. Extract named entities from the text.

Return ONLY a JSON object in this exact format (no explanation, no markdown):
{"entities": [{"entity": "exact text from article", "label": "WEAPON"}]}

Labels to use:
- WEAPON : missiles, aircraft, tanks, ships, guns, defense systems (ex: Kalibr, S-400, Su-35, T-90)
- MIL_UNIT : military units, groups, fleets, battalions (ex: Black Sea Fleet, Vostok group)
- MIL_ORG : military organizations, ministries, alliances (ex: NATO, Ministry of Defense, Rostec)

If no military entities found, return: {"entities": []}"""

def annotate_one(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": f"Extract military entities from this text:\n\n{text[:800]}"}
            ],
            temperature=0,
            max_tokens=500
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r'```json\s*', '', raw)
        raw = re.sub(r'```\s*', '', raw).strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return data.get("entities", [])
        return []
    except Exception as e:
        return []

def find_positions(text, entity):
    idx = text.lower().find(entity.lower())
    if idx == -1:
        return None, None
    return idx, idx + len(entity)

def format_duration(seconds):
    return str(timedelta(seconds=int(seconds)))

# ── Chargement ────────────────────────────────────────────────────────────────
print("📥 Chargement du corpus...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    corpus = json.load(f)

textes = corpus[:MAX_ARTICLES]
print(f"✅ {len(textes)} articles à annoter\n")
print("🤖 Annotation avec Llama-3.1 (Groq)...\n")

annotations_llm = []
skipped = 0
temps_par_article = []
start_total = time.time()

for i, texte in enumerate(textes):
    texte_court = texte[:800]

    # Chrono par article
    t0 = time.time()
    entities_raw = annotate_one(texte_court)
    duree_article = time.time() - t0
    temps_par_article.append(duree_article)

    spans = []
    for ent in entities_raw:
        label = ent.get("label", "")
        entity_text = ent.get("entity", "")
        if label in {"WEAPON", "MIL_UNIT", "MIL_ORG"} and entity_text:
            start, end = find_positions(texte_court, entity_text)
            if start is not None:
                spans.append((start, end, label))

    if spans:
        annotations_llm.append((texte_court, {"entities": spans}))
    else:
        skipped += 1

    # Progression toutes les 50 articles
    if (i + 1) % 50 == 0 or (i + 1) == len(textes):
        elapsed     = time.time() - start_total
        avg_speed   = elapsed / (i + 1)
        remaining   = avg_speed * (len(textes) - i - 1)
        vitesse_moy = sum(temps_par_article[-50:]) / len(temps_par_article[-50:])

        print(f"  ✔ {i+1:>3}/{len(textes)} articles"
              f" | annotés : {len(annotations_llm)}"
              f" | temps/article : {vitesse_moy:.2f}s"
              f" | écoulé : {format_duration(elapsed)}"
              f" | restant : {format_duration(remaining)}")

    time.sleep(0.3)

# ── Stats finales ─────────────────────────────────────────────────────────────
total_elapsed = time.time() - start_total
counts = {"WEAPON": 0, "MIL_UNIT": 0, "MIL_ORG": 0}
for _, data in annotations_llm:
    for _, _, label in data["entities"]:
        counts[label] += 1

print(f"\n⏱️  Temps total : {format_duration(total_elapsed)}")
print(f"   Temps moyen par article : {sum(temps_par_article)/len(temps_par_article):.2f}s")

print(f"\n📊 Résultats LLM :")
print(f"  Articles annotés     : {len(annotations_llm)}")
print(f"  Articles sans entité : {skipped}")
print(f"\n  WEAPON    : {counts['WEAPON']}")
print(f"  MIL_UNIT  : {counts['MIL_UNIT']}")
print(f"  MIL_ORG   : {counts['MIL_ORG']}")
print(f"  TOTAL     : {sum(counts.values())}")

# ── Sauvegarde ────────────────────────────────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(annotations_llm, f, ensure_ascii=False, indent=2)

print(f"\n✅ {OUTPUT_FILE} sauvegardé !")
print("➡️  Lance step3c_comparaison.py pour comparer avec rule-based !")
