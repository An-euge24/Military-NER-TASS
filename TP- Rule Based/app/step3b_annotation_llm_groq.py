"""
Étape 3b, annotation des articles avec un LLM via Groq.

Entrée :
    data/data_set_nettoyé.json

Sorties :
    data/annotations_llm.json
    logs/step3b_llm_metrics.json
    logs/step3b_llm_console.log

Test initial :
    MAX_ARTICLES = 10

Après validation :
    MAX_ARTICLES = 800
"""

import json
import os
import re
import time
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ============================================================================
# CHEMINS DU PROJET
# ============================================================================

# Le script se trouve dans :
# projet/app/step3b_annotation_llm_groq.py

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

INPUT_FILE = DATA_DIR / "data_set_nettoyé.json"
OUTPUT_FILE = DATA_DIR / "annotations_llm.json"
METRICS_FILE = LOGS_DIR / "step3b_llm_metrics.json"
ENV_FILE = BASE_DIR / ".env"


# ============================================================================
# PARAMÈTRES
# ============================================================================

# Test initial sur 10 articles.
# Après validation, modifier cette valeur en 800.
MAX_ARTICLES = 800

# Même limite que dans les autres étapes du projet.
MAX_CHARACTERS = 800

# Modèle Groq utilisé.
MODEL_NAME = "openai/gpt-oss-20b"

# Pause entre deux appels API.
SLEEP_BETWEEN_REQUESTS = 0.3

ALLOWED_LABELS = {
    "WEAPON",
    "MIL_UNIT",
    "MIL_ORG",
}


# ============================================================================
# CHARGEMENT DE LA CLÉ API
# ============================================================================

load_dotenv(
    ENV_FILE,
    override=True,
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY est absente du fichier .env. "
        "Ajoute une clé Groq valide dans le fichier .env."
    )

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================================
# PROMPT LLM
# ============================================================================

SYSTEM_PROMPT = """
You are a military named entity recognition expert.

Extract military entities from the article.

Return only one valid JSON object using exactly this structure:

{
  "entities": [
    {
      "entity": "exact text from the article",
      "label": "WEAPON"
    }
  ]
}

Allowed labels:

- WEAPON:
  missiles, aircraft, tanks, ships, guns and defense systems.
  Examples: Kalibr, S-400, Su-35, T-90.

- MIL_UNIT:
  military units, groups, fleets and battalions.
  Examples: Black Sea Fleet, Vostok group.

- MIL_ORG:
  military organizations, ministries and alliances.
  Examples: NATO, Ministry of Defense, Rostec.

If no military entity is found, return exactly:

{
  "entities": []
}

Do not add explanations.
Do not use Markdown.
Do not use code fences.
Return only valid JSON.
"""


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def format_duration(seconds):
    """Convertit une durée en format lisible."""
    return str(timedelta(seconds=int(seconds)))


def normalize_text(article):
    """
    Transforme un article en texte.

    Le corpus contient normalement des chaînes de caractères.
    Cette fonction accepte aussi quelques formats dictionnaires.
    """
    if isinstance(article, str):
        return article

    if isinstance(article, dict):
        for key in ("text", "content", "article", "body"):
            value = article.get(key)

            if isinstance(value, str):
                return value

    return str(article)


def find_positions(text, entity):
    """
    Recherche la position de la première occurrence d'une entité.
    """
    if not entity:
        return None, None

    index = text.lower().find(entity.lower())

    if index == -1:
        return None, None

    return index, index + len(entity)


def parse_json_response(raw_response):
    """
    Transforme la réponse LLM en objet JSON.

    Le mode json_object devrait produire directement du JSON valide.
    Une recherche de secours est conservée si le modèle ajoute
    accidentellement du texte autour de l'objet JSON.
    """
    if not raw_response:
        raise ValueError("Réponse LLM vide")

    cleaned = raw_response.strip()

    # Premier essai : la réponse complète est un JSON valide.
    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        pass

    # Suppression éventuelle des blocs Markdown.
    cleaned = re.sub(
        r"```json\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"```\s*",
        "",
        cleaned,
    ).strip()

    # Recherche d'un objet JSON dans la réponse.
    match = re.search(
        r"\{.*\}",
        cleaned,
        flags=re.DOTALL,
    )

    if not match:
        raise ValueError(
            "Aucun objet JSON détecté dans la réponse LLM"
        )

    return json.loads(match.group())


def annotate_one(text):
    """
    Envoie un article au modèle Groq.

    Retourne :
        entities, error_message
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": (
                        "Extract military entities from this article:\n\n"
                        f"{text[:MAX_CHARACTERS]}"
                    ),
                },
            ],
            temperature=0,
            max_completion_tokens=2048,
            reasoning_effort="low",
            include_reasoning=False,
            response_format={
                "type": "json_object",
            },
        )

        raw_content = (
            response.choices[0].message.content or ""
        )

        data = parse_json_response(raw_content)

        entities = data.get("entities", [])

        if not isinstance(entities, list):
            raise ValueError(
                "Le champ 'entities' n'est pas une liste"
            )

        return entities, None

    except Exception as error:
        error_message = (
            f"{type(error).__name__}: "
            f"{str(error)[:250]}"
        )

        return [], error_message


# ============================================================================
# PROGRAMME PRINCIPAL
# ============================================================================

def main():
    start_total = time.time()

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    LOGS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("📥 Chargement du corpus...")
    print(f"📁 Fichier d'entrée : {INPUT_FILE}")
    print(f"🤖 Modèle utilisé : {MODEL_NAME}")
    print(f"📏 Limite par article : {MAX_CHARACTERS} caractères")
    print(f"🔢 Nombre d'articles du test : {MAX_ARTICLES}")
    print()

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        corpus = json.load(file)

    if not isinstance(corpus, list):
        raise ValueError(
            "Le corpus doit être une liste d'articles"
        )

    textes = [
        normalize_text(article)[:MAX_CHARACTERS]
        for article in corpus[:MAX_ARTICLES]
    ]

    print(
        f"✅ {len(textes)} article(s) à annoter"
    )
    print()

    annotations_llm = []
    articles_without_entities = 0
    api_or_json_errors = 0
    error_examples = []

    processing_times = []

    entity_counts = {
        "WEAPON": 0,
        "MIL_UNIT": 0,
        "MIL_ORG": 0,
    }

    progress_step = 10

    for index, text in enumerate(
        textes,
        start=1,
    ):
        start_article = time.time()

        entities_raw, error_message = annotate_one(text)

        duration_article = time.time() - start_article
        processing_times.append(duration_article)

        if error_message:
            api_or_json_errors += 1

            if len(error_examples) < 5:
                error_examples.append(
                    {
                        "article_number": index,
                        "error": error_message,
                    }
                )

            print(
                f"⚠️ Article {index}, erreur LLM : "
                f"{error_message}"
            )

        spans = []

        for entity in entities_raw:
            if not isinstance(entity, dict):
                continue

            label = entity.get("label", "")
            entity_text = str(
                entity.get("entity", "")
            ).strip()

            if label not in ALLOWED_LABELS:
                continue

            if not entity_text:
                continue

            start_position, end_position = find_positions(
                text,
                entity_text,
            )

            if start_position is None:
                continue

            spans.append(
                (
                    start_position,
                    end_position,
                    label,
                )
            )

            entity_counts[label] += 1

        if spans:
            annotations_llm.append(
                (
                    text,
                    {
                        "entities": spans,
                    },
                )
            )

        else:
            articles_without_entities += 1

        if (
            index % progress_step == 0
            or index == len(textes)
        ):
            elapsed = time.time() - start_total
            average_time = elapsed / index
            remaining = average_time * (
                len(textes) - index
            )

            print(
                f"✔ {index}/{len(textes)} articles"
                f" | annotés : {len(annotations_llm)}"
                f" | temps/article : "
                f"{duration_article:.2f}s"
                f" | écoulé : "
                f"{format_duration(elapsed)}"
                f" | restant estimé : "
                f"{format_duration(remaining)}"
            )

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    total_elapsed = time.time() - start_total
    total_entities = sum(entity_counts.values())

    average_seconds = 0

    if processing_times:
        average_seconds = (
            sum(processing_times)
            / len(processing_times)
        )

    # =========================================================================
    # SAUVEGARDE DES ANNOTATIONS
    # =========================================================================

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            annotations_llm,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # =========================================================================
    # SAUVEGARDE DES MÉTRIQUES
    # =========================================================================

    metrics = {
        "method": "LLM",
        "provider": "Groq",
        "model": MODEL_NAME,
        "input_file": str(INPUT_FILE),
        "output_file": str(OUTPUT_FILE),
        "input_articles_total": len(corpus),
        "processed_articles": len(textes),
        "annotated_articles": len(annotations_llm),
        "articles_without_entities": (
            articles_without_entities
        ),
        "api_or_json_errors": api_or_json_errors,
        "entity_counts": entity_counts,
        "total_entities": total_entities,
        "max_characters_per_article": MAX_CHARACTERS,
        "duration_seconds": round(
            total_elapsed,
            2,
        ),
        "average_seconds_per_article": round(
            average_seconds,
            2,
        ),
        "error_examples": error_examples,
    }

    with METRICS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # =========================================================================
    # RÉSUMÉ FINAL
    # =========================================================================

    print()
    print("✅ Annotation LLM terminée")
    print(
        f"📊 Articles annotés : "
        f"{len(annotations_llm)}"
    )
    print(
        "📄 Articles sans entité : "
        f"{articles_without_entities}"
    )
    print()
    print(
        f"WEAPON   : "
        f"{entity_counts['WEAPON']}"
    )
    print(
        f"MIL_UNIT : "
        f"{entity_counts['MIL_UNIT']}"
    )
    print(
        f"MIL_ORG  : "
        f"{entity_counts['MIL_ORG']}"
    )
    print(
        f"TOTAL    : {total_entities}"
    )
    print()
    print(
        f"⏱️ Durée totale : "
        f"{format_duration(total_elapsed)}"
    )
    print(
        f"💾 Résultats : {OUTPUT_FILE}"
    )
    print(
        f"📈 Métriques : {METRICS_FILE}"
    )
    print(
        f"⚠️ Erreurs API ou JSON : "
        f"{api_or_json_errors}"
    )


if __name__ == "__main__":
    main()