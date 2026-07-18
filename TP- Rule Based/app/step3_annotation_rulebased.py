"""
Étape 3 — Annotation automatique par règles (spaCy EntityRuler)
Aucun téléchargement requis !
Input  : data_set_nettoyé.json   (800 textes)
Output : annotations_spacy.json  (format spaCy prêt pour l'entraînement)

Installation préalable :
    pip install spacy
    python -m spacy download en_core_web_sm
"""

import json
import spacy                           # bibliothèque de traitement du langage naturel
from spacy.pipeline import EntityRuler #permet d'ajouter un composant de règles d'entités à un pipeline spaCy

# ── Chargement de spaCy ───────────────────────────────────────────────────────
print("⏳ Chargement de spaCy...")
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler", before="ner")

# ── Dictionnaire d'entités militaires ────────────────────────────────────────
patterns = [

    # WEAPONS — missiles
    {"label": "WEAPON", "pattern": "Kalibr"},
    {"label": "WEAPON", "pattern": "Iskander"},
    {"label": "WEAPON", "pattern": "Kinzhal"},
    {"label": "WEAPON", "pattern": "Zircon"},
    {"label": "WEAPON", "pattern": "Oniks"},
    {"label": "WEAPON", "pattern": "Kh-101"},
    {"label": "WEAPON", "pattern": "Kh-555"},
    {"label": "WEAPON", "pattern": "Kh-22"},
    {"label": "WEAPON", "pattern": "Kh-47"},
    {"label": "WEAPON", "pattern": "X-101"},
    {"label": "WEAPON", "pattern": "Tornado-G"},
    {"label": "WEAPON", "pattern": "Tornado-S"},
    {"label": "WEAPON", "pattern": "Uragan"},
    {"label": "WEAPON", "pattern": "Smerch"},
    {"label": "WEAPON", "pattern": "Grad"},
    {"label": "WEAPON", "pattern": "Lancet"},
    {"label": "WEAPON", "pattern": "Geran"},

    # WEAPONS — systèmes de défense aérienne
    {"label": "WEAPON", "pattern": "S-400"},
    {"label": "WEAPON", "pattern": "S-300"},
    {"label": "WEAPON", "pattern": "S-500"},
    {"label": "WEAPON", "pattern": "Buk"},
    {"label": "WEAPON", "pattern": "Buk-M2"},
    {"label": "WEAPON", "pattern": "Buk-M3"},
    {"label": "WEAPON", "pattern": "Tor"},
    {"label": "WEAPON", "pattern": "Pantsir"},
    {"label": "WEAPON", "pattern": "Pantsir-S1"},
    {"label": "WEAPON", "pattern": "Derivatsia-PVO"},
    {"label": "WEAPON", "pattern": "Triumf"},
    {"label": "WEAPON", "pattern": "Morfei"},

    # WEAPONS — chars et véhicules
    {"label": "WEAPON", "pattern": "T-90"},
    {"label": "WEAPON", "pattern": "T-80"},
    {"label": "WEAPON", "pattern": "T-72"},
    {"label": "WEAPON", "pattern": "T-14"},
    {"label": "WEAPON", "pattern": "Armata"},
    {"label": "WEAPON", "pattern": "BMP-3"},
    {"label": "WEAPON", "pattern": "BTR-82"},
    {"label": "WEAPON", "pattern": "Terminator"},

    # WEAPONS — avions et hélicoptères
    {"label": "WEAPON", "pattern": "Su-35"},
    {"label": "WEAPON", "pattern": "Su-30"},
    {"label": "WEAPON", "pattern": "Su-57"},
    {"label": "WEAPON", "pattern": "Su-25"},
    {"label": "WEAPON", "pattern": "Su-34"},
    {"label": "WEAPON", "pattern": "Su-27"},
    {"label": "WEAPON", "pattern": "Su-30SM"},
    {"label": "WEAPON", "pattern": "MiG-31"},
    {"label": "WEAPON", "pattern": "Ka-52"},
    {"label": "WEAPON", "pattern": "Mi-28"},
    {"label": "WEAPON", "pattern": "Mi-35"},
    {"label": "WEAPON", "pattern": "Ansat"},

    # WEAPONS — sous-marins et navires
    {"label": "WEAPON", "pattern": "Yasen-M"},
    {"label": "WEAPON", "pattern": "Project 885M"},
    {"label": "WEAPON", "pattern": "Borei"},
    {"label": "WEAPON", "pattern": "Kalibr-PL"},

    # MIL_UNIT — unités russes
    {"label": "MIL_UNIT", "pattern": "Vostok"},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Vostok"}, {"TEXT": "group"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Southern"}, {"TEXT": "Group"}, {"TEXT": "of"}, {"TEXT": "Forces"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Northern"}, {"TEXT": "Fleet"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Black"}, {"TEXT": "Sea"}, {"TEXT": "Fleet"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Pacific"}, {"TEXT": "Fleet"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Baltic"}, {"TEXT": "Fleet"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Caspian"}, {"TEXT": "Flotilla"}]},
    {"label": "MIL_UNIT", "pattern": "Battlegroup"},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Battlegroup"}, {"TEXT": "South"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Battlegroup"}, {"TEXT": "North"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Battlegroup"}, {"TEXT": "Center"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Battlegroup"}, {"TEXT": "East"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Battlegroup"}, {"TEXT": "West"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Aerospace"}, {"TEXT": "Forces"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Airborne"}, {"TEXT": "Forces"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Armed"}, {"TEXT": "Forces"}, {"TEXT": "of"}, {"TEXT": "Ukraine"}]},
    {"label": "MIL_UNIT", "pattern": [{"TEXT": "Armed"}, {"TEXT": "Forces"}, {"TEXT": "of"}, {"TEXT": "Russia"}]},

    # MIL_ORG — organisations militaires
    {"label": "MIL_ORG", "pattern": [{"TEXT": "Russian"}, {"TEXT": "Defense"}, {"TEXT": "Ministry"}]},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "Defense"}, {"TEXT": "Ministry"}]},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "Ministry"}, {"TEXT": "of"}, {"TEXT": "Defense"}]},
    {"label": "MIL_ORG", "pattern": "NATO"},
    {"label": "MIL_ORG", "pattern": "CSTO"},
    {"label": "MIL_ORG", "pattern": "FSB"},
    {"label": "MIL_ORG", "pattern": "GRU"},
    {"label": "MIL_ORG", "pattern": "SVR"},
    {"label": "MIL_ORG", "pattern": "Rostec"},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "Almaz"}, {"TEXT": "-"}, {"TEXT": "Antey"}]},
    {"label": "MIL_ORG", "pattern": "Rosoboronexport"},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "Russian"}, {"TEXT": "Helicopters"}]},
    {"label": "MIL_ORG", "pattern": "Pentagon"},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "General"}, {"TEXT": "Staff"}]},
    {"label": "MIL_ORG", "pattern": [{"TEXT": "National"}, {"TEXT": "Guard"}]},
]

ruler.add_patterns(patterns)

# ── Chargement du corpus ─────────────────────────────────────────────────────
with open('../data/data_set_nettoyé.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

print(f"📥 {len(corpus)} articles à annoter\n")

# ── Annotation ────────────────────────────────────────────────────────────────
annotations_spacy = []
skipped = 0

for i, texte in enumerate(corpus):
    texte_tronque = texte[:1000]
    doc = nlp(texte_tronque)

    spans = []
    for ent in doc.ents:
        if ent.label_ in {"WEAPON", "MIL_UNIT", "MIL_ORG"}:
            spans.append((ent.start_char, ent.end_char, ent.label_))

    # Garder uniquement les articles avec au moins 1 entité
    if spans:
        annotations_spacy.append((texte_tronque, {"entities": spans}))
    else:
        skipped += 1

    if (i + 1) % 50 == 0:
        print(f"  ✔ {i+1}/800 articles traités...")

# ── Statistiques ─────────────────────────────────────────────────────────────
print(f"\n✅ Annotation terminée")
print(f"  Articles annotés  : {len(annotations_spacy)}")
print(f"  Articles sans entité : {skipped} (exclus)")

counts = {"WEAPON": 0, "MIL_UNIT": 0, "MIL_ORG": 0}
for _, data in annotations_spacy:
    for _, _, label in data["entities"]:
        counts[label] += 1

print("\n📊 Entités détectées :")
for label, count in counts.items():
    print(f"  {label:10} : {count}")
print(f"  {'TOTAL':10} : {sum(counts.values())}")

# ── Sauvegarde ────────────────────────────────────────────────────────────────
with open('../data/annotations_spacy.json', 'w', encoding='utf-8') as f:
    json.dump(annotations_spacy, f, ensure_ascii=False, indent=2)

print(f"\n✅ ../data/annotations_spacy.json sauvegardé — prêt pour l'entraînement spaCy !")
