"""Inférence complète avec logs de chargement, volume et durée.

À placer dans le dossier app/ du projet. La limite MAX_TEXT_LENGTH est conservée
pour rendre explicite le périmètre de l’expérimentation actuelle.
"""
import json, re, time
from pathlib import Path
import spacy

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "data_set.json"
MODEL_DIR = BASE_DIR / "model_ner"
OUTPUT_FILE = BASE_DIR / "data" / "resultats_inference.json"
LOG_DIR = BASE_DIR / "logs"; LOG_DIR.mkdir(exist_ok=True)
MAX_TEXT_LENGTH = 1000

start_total = time.perf_counter()
start_model = time.perf_counter()
print(f"⏳ Chargement du modèle : {MODEL_DIR}")
nlp = spacy.load(MODEL_DIR)
model_load_s = time.perf_counter() - start_model
print(f"✅ Modèle chargé en {model_load_s:.2f} s\n")

start_data = time.perf_counter()
print(f"📥 Chargement du corpus : {INPUT_FILE}")
with INPUT_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)
articles = [a for a in data if a.get("text") and len(a["text"].strip()) > 100]
data_load_s = time.perf_counter() - start_data
print(f"✅ {len(articles)} articles valides en {data_load_s:.2f} s\n")

def clean_text(text):
    text = re.sub(r'^[A-Z][A-Z ,\-]+,\s+\w+ \d+\.\s*/TASS/\.\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()

print(f"🔍 Inférence en cours, limite documentaire : {MAX_TEXT_LENGTH} caractères")
resultats=[]; counts={"WEAPON":0,"MIL_UNIT":0,"MIL_ORG":0}
start_inference=time.perf_counter()
for i,article in enumerate(articles):
    texte=clean_text(article.get("text") or "")[:MAX_TEXT_LENGTH]
    doc=nlp(texte)
    entities=[]
    for ent in doc.ents:
        if ent.label_ in counts:
            entities.append({"entity":ent.text,"label":ent.label_,"start":ent.start_char,"end":ent.end_char})
            counts[ent.label_]+=1
    out=dict(article); out["text_clean"]=texte; out["entities"]=entities; resultats.append(out)
    if (i+1)%2000==0: print(f"  ✔ {i+1}/{len(articles)} articles traités...")
inference_s=time.perf_counter()-start_inference
with OUTPUT_FILE.open("w",encoding="utf-8") as f: json.dump(resultats,f,ensure_ascii=False,indent=2)
articles_with=sum(1 for r in resultats if r["entities"])
total_s=time.perf_counter()-start_total
metrics={"articles_traitees":len(resultats),"articles_avec_entites":articles_with,"articles_sans_entite":len(resultats)-articles_with,"entites_par_label":counts,"entites_total":sum(counts.values()),"model_load_seconds":round(model_load_s,2),"data_load_seconds":round(data_load_s,2),"inference_seconds":round(inference_s,2),"total_seconds":round(total_s,2),"throughput_articles_per_second":round(len(resultats)/inference_s,2) if inference_s else None,"output_size_bytes":OUTPUT_FILE.stat().st_size,"max_text_length":MAX_TEXT_LENGTH}
with (LOG_DIR/"inference_metrics.json").open("w",encoding="utf-8") as f: json.dump(metrics,f,ensure_ascii=False,indent=2)
print(f"\n📊 Articles traités : {len(resultats)} | avec entités : {articles_with} | sans entité : {len(resultats)-articles_with}")
print(f"📊 WEAPON={counts['WEAPON']} | MIL_UNIT={counts['MIL_UNIT']} | MIL_ORG={counts['MIL_ORG']} | TOTAL={sum(counts.values())}")
print(f"⏱️ Chargement modèle : {model_load_s:.2f} s | données : {data_load_s:.2f} s | inférence : {inference_s:.2f} s | total : {total_s:.2f} s")
print(f"💾 Sortie : {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} octets)")
