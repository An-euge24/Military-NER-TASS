"""Indexation locale Elasticsearch pour la démonstration de soutenance.

La sortie JSON locale reste la preuve principale. Ce script ne supprime pas
l'index existant sauf si RESET_INDEX=true est fourni explicitement.
"""
from datetime import datetime, timezone
import time
import json
import os
from pathlib import Path
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
ES_URL = os.getenv("ES_URL", "http://localhost:9200")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")
INDEX = os.getenv("INDEX", "tass_articles_soutenance_2026")
RESET_INDEX = os.getenv("RESET_INDEX", "false").lower() == "true"
DATA_PATH = Path(os.getenv("RESULTS_JSON", ROOT / "data" / "resultats_inference.json"))


def build_client():
    auth = (ES_USER, ES_PASS) if ES_USER and ES_PASS else None
    return Elasticsearch(ES_URL, basic_auth=auth, request_timeout=60)


def mapping():
    return {
        "mappings": {"properties": {
            "id": {"type": "keyword"},
            "date": {"type": "date", "format": "yyyy-MM-dd||epoch_second"},
            "title": {"type": "text"},
            "text_clean": {"type": "text"},
            "link": {"type": "keyword"},
            "weapons": {"type": "keyword"},
            "mil_units": {"type": "keyword"},
            "mil_orgs": {"type": "keyword"},
            "nb_entities": {"type": "integer"},
        }}
    }


def documents(articles):
    for article in articles:
        weapons = sorted({e["entity"] for e in article.get("entities", []) if e.get("label") == "WEAPON"})
        units = sorted({e["entity"] for e in article.get("entities", []) if e.get("label") == "MIL_UNIT"})
        orgs = sorted({e["entity"] for e in article.get("entities", []) if e.get("label") == "MIL_ORG"})
        date_val = article.get("date")
        if isinstance(date_val, int):
            date_val = datetime.fromtimestamp(date_val, tz=timezone.utc).strftime("%Y-%m-%d")
        yield {"_index": INDEX, "_source": {
            "id": str(article.get("id", "")),
            "date": date_val,
            "title": (article.get("title") or "").strip(),
            "text_clean": article.get("text_clean", ""),
            "link": article.get("link", ""),
            "weapons": weapons,
            "mil_units": units,
            "mil_orgs": orgs,
            "nb_entities": len(weapons) + len(units) + len(orgs),
        }}


def main():
    total_start = time.perf_counter()
    print(f"Connexion à Elasticsearch local : {ES_URL}")
    connection_start = time.perf_counter()
    es = build_client()
    connection_s = time.perf_counter() - connection_start
    print(f"Temps de connexion : {connection_s:.2f} s")
    if not es.ping():
        raise SystemExit("Connexion impossible. Vérifier Docker et le port 9200.")
    if es.indices.exists(index=INDEX):
        if RESET_INDEX:
            es.indices.delete(index=INDEX)
            print(f"Index existant supprimé : {INDEX}")
        else:
            raise SystemExit(f"L'index {INDEX} existe déjà. Utiliser RESET_INDEX=true uniquement si nécessaire.")
    es.indices.create(index=INDEX, body=mapping())
    with DATA_PATH.open("r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Articles chargés : {len(articles)}")
    bulk_start = time.perf_counter()
    success, errors = helpers.bulk(es, documents(articles), chunk_size=500, raise_on_error=False)
    bulk_s = time.perf_counter() - bulk_start
    es.indices.refresh(index=INDEX)
    count = es.count(index=INDEX)["count"]
    print(f"Documents indexés : {success}")
    print(f"Erreurs : {len(errors) if errors else 0}")
    total_s = time.perf_counter() - total_start
    print(f"Documents présents dans {INDEX} : {count}")
    print(f"Temps indexation : {bulk_s:.2f} s | temps total : {total_s:.2f} s")


if __name__ == "__main__":
    main()
