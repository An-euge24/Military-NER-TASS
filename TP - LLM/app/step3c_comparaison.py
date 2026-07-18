"""
Étape 3c — Comparaison Rule-Based vs LLM
Input  : ../data/annotations_spacy.json  (méthode rule-based)
         ../data/annotations_llm.json    (méthode LLM Groq)
Output : ../data/rapport_comparaison.txt
"""

import json #bibliothèque pour manipuler des fichiers JSON

def load_entities(filepath):        #permet de charger les entités détectées dans un fichier JSON
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    entities = {"WEAPON": set(), "MIL_UNIT": set(), "MIL_ORG": set()}
    counts   = {"WEAPON": 0,   "MIL_UNIT": 0,   "MIL_ORG": 0}
    for text, annot in data:
        for start, end, label in annot["entities"]:
            term = text[start:end].lower().strip()
            entities[label].add(term)
            counts[label] += 1
    return entities, counts, len(data)

print("📊 Chargement des deux fichiers...")
rb_ents, rb_counts, rb_articles = load_entities("../data/annotations_spacy.json")
llm_ents, llm_counts, llm_articles = load_entities("../data/annotations_llm.json")

lines = [] #permet de stocker les lignes du rapport de comparaison, c'est une liste de chaînes de caractères qui sera ensuite jointe pour créer le rapport final
lines.append("=" * 60)
lines.append("COMPARAISON RULE-BASED vs LLM (Groq Llama-3)")
lines.append("=" * 60)

lines.append(f"\n{'':25} {'Rule-Based':>12} {'LLM':>12}")
lines.append("-" * 50)
lines.append(f"{'Articles annotés':25} {rb_articles:>12} {llm_articles:>12}")
for label in ["WEAPON", "MIL_UNIT", "MIL_ORG"]:
    lines.append(f"  {label:23} {rb_counts[label]:>12} {llm_counts[label]:>12}")
total_rb  = sum(rb_counts.values())
total_llm = sum(llm_counts.values())
lines.append(f"{'TOTAL entités':25} {total_rb:>12} {total_llm:>12}")
lines.append(f"{'Termes uniques WEAPON':25} {len(rb_ents['WEAPON']):>12} {len(llm_ents['WEAPON']):>12}")
lines.append(f"{'Termes uniques MIL_UNIT':25} {len(rb_ents['MIL_UNIT']):>12} {len(llm_ents['MIL_UNIT']):>12}")
lines.append(f"{'Termes uniques MIL_ORG':25} {len(rb_ents['MIL_ORG']):>12} {len(llm_ents['MIL_ORG']):>12}")

for label in ["WEAPON", "MIL_UNIT", "MIL_ORG"]:
    only_llm = llm_ents[label] - rb_ents[label]
    lines.append(f"\n🆕 {label} — termes détectés UNIQUEMENT par le LLM ({len(only_llm)}) :")
    for t in sorted(only_llm)[:20]:
        lines.append(f"   - {t}")
    if len(only_llm) > 20:
        lines.append(f"   ... et {len(only_llm)-20} autres")

    only_rb = rb_ents[label] - llm_ents[label]
    lines.append(f"\n📌 {label} — termes détectés UNIQUEMENT par Rule-Based ({len(only_rb)}) :")
    for t in sorted(only_rb)[:10]:
        lines.append(f"   - {t}")

report = "\n".join(lines)
print(report)

with open("../data/rapport_comparaison.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\n✅ ../data/rapport_comparaison.txt sauvegardé !")
