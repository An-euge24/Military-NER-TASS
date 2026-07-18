"""
Étape 6a — Ingestion dans Elasticsearch (Elastic Cloud)
Input  : resultats_inference.json  (dataset enrichi avec entités)
Output : Index Elasticsearch "tass_articles"

Installation préalable :
    pip install elasticsearch
"""

from elasticsearch import Elasticsearch, helpers
import json
from dotenv import load_dotenv
import os

# ── ⚠️ REMPLIS TES IDENTIFIANTS ICI ─────────────────────────────────────────
load_dotenv()
CLOUD_ID = os.getenv("CLOUD_ID")
ES_USER  = os.getenv("ES_USER")
ES_PASS  = os.getenv("ES_PASS")
INDEX    = os.getenv("INDEX")


# ── Connexion à Elastic Cloud ─────────────────────────────────────────────────
print("⏳ Connexion à Elastic Cloud...")
es = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=(ES_USER, ES_PASS)
)

if not es.ping():
    print("❌ Connexion échouée — vérifie ton Cloud ID et ton mot de passe")
    exit(1)

print("✅ Connecté à Elastic Cloud\n")

# ── Création de l'index avec mapping ─────────────────────────────────────────
mapping = {
    "mappings": {
        "properties": {
            "id":         {"type": "keyword"},
            "date":       {"type": "date", "format": "yyyy-MM-dd||epoch_second"},
            "title":      {"type": "text"},
            "text_clean": {"type": "text"},
            "link":       {"type": "keyword"},
            "weapons":    {"type": "keyword"},   # liste des armes citées
            "mil_units":  {"type": "keyword"},   # liste des unités militaires
            "mil_orgs":   {"type": "keyword"},   # liste des organisations
            "nb_entities":{"type": "integer"}    # nombre total d'entités
        }
    }
}

# Supprimer l'index s'il existe déjà (pour recommencer proprement)
if es.indices.exists(index=INDEX):
    es.indices.delete(index=INDEX)
    print(f"🗑️  Index '{INDEX}' existant supprimé")

es.indices.create(index=INDEX, body=mapping)
print(f"✅ Index '{INDEX}' créé avec le mapping\n")

# ── Chargement des données ────────────────────────────────────────────────────
print("📥 Chargement de resultats_inference.json...")
with open("../data/resultats_inference.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"✅ {len(articles)} articles chargés\n")

# ── Préparation des documents pour l'indexation ──────────────────────────────
def prepare_documents(articles):
    for article in articles:
        # Séparer les entités par type
        weapons   = list(set(e["entity"] for e in article.get("entities", []) if e["label"] == "WEAPON"))
        mil_units = list(set(e["entity"] for e in article.get("entities", []) if e["label"] == "MIL_UNIT"))
        mil_orgs  = list(set(e["entity"] for e in article.get("entities", []) if e["label"] == "MIL_ORG"))

        # Convertir la date timestamp en format ISO si nécessaire
        date_val = article.get("date")
        if isinstance(date_val, int):
            from datetime import datetime, timezone
            date_val = datetime.fromtimestamp(date_val, tz=timezone.utc).strftime("%Y-%m-%d")

        doc = {
            "_index": INDEX,
            "_source": {
                "id":          str(article.get("id", "")),
                "date":        date_val,
                "title":       (article.get("title") or "").strip(),
                "text_clean":  article.get("text_clean", ""),
                "link":        article.get("link", ""),
                "weapons":     weapons,
                "mil_units":   mil_units,
                "mil_orgs":    mil_orgs,
                "nb_entities": len(weapons) + len(mil_units) + len(mil_orgs)
            }
        }
        yield doc

# ── Indexation par bulk ───────────────────────────────────────────────────────
print("🚀 Indexation en cours...")

success, errors = helpers.bulk(
    es,
    prepare_documents(articles),
    chunk_size=500,
    raise_on_error=False
)

print(f"\n📊 Résultats de l'indexation :")
print(f"  ✅ Documents indexés : {success}")
if errors:
    print(f"  ❌ Erreurs          : {len(errors)}")

# ── Vérification finale ───────────────────────────────────────────────────────
count = es.count(index=INDEX)["count"]
print(f"\n✅ Index '{INDEX}' contient {count} documents")
print(f"🎉 Ingestion terminée — prêt pour les dashboards Kibana !")
