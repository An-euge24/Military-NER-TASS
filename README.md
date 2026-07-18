# 🎖️ Military NER — Analyse des articles TASS

> Pipeline NLP complet pour l'extraction d'entités militaires dans des articles de presse russes (TASS), appliqué au conflit russo-ukrainien.  
> Projet réalisé dans le cadre du cours **AI Deployment** — Eugenia School 2025/2026

---

## 📌 Objectif

Construire un pipeline de **Named Entity Recognition (NER)** capable de détecter automatiquement trois types d'entités militaires dans des articles de presse :

| Label | Description | Exemples |
|---|---|---|
| `WEAPON` | Missiles, aéronefs, chars, systèmes de défense | S-400, Kalibr, Su-57, Ka-52 |
| `MIL_UNIT` | Unités militaires, flottes, groupes de combat | Baltic Fleet, Battlegroup East |
| `MIL_ORG` | Organisations, ministères, alliances | NATO, Rostec, Defense Ministry |

Ce projet compare **deux méthodes d'annotation** pour entraîner un modèle NER :

| | TP-LLM | TP-RuleBased ✅ |
|---|---|---|
| **Méthode** | Annotation par LLM (Groq Llama-3.1) | Annotation par dictionnaire (EntityRuler) |
| **F1-score** | ~42% | **84.3%** |
| **Méthode retenue** | ❌ | ✅ |

---

## 📁 Structure du projet

```
Military-NER-TASS/
│
├── README.md
├── .gitignore
│
├── TP-LLM/                               ← Méthode par LLM (comparaison)
│   ├── app/
│   │   ├── step2_extraction.py           # Nettoyage du corpus
│   │   ├── step3_annotation_rulebased.py # Annotation Rule-Based (base de comparaison)
│   │   ├── step3b_annotation_llm_groq.py # Annotation LLM (Groq - Llama-3.1)
│   │   ├── step3c_comparaison.py         # Rapport comparatif Rule-Based vs LLM
│   │   └── step4a_convert_spacy.py       # Conversion annotations → .spacy (DocBin)
│   ├── data/
│   │   ├── annotations_llm.json          # 384 articles annotés par LLM
│   │   ├── annotations_spacy.json        # 516 articles annotés Rule-Based
│   │   ├── rapport_comparaison.txt       # Rapport statistique comparatif
│   │   ├── train.spacy                   # Données entraînement (80%)
│   │   └── dev.spacy                     # Données validation (20%)
│   └── config.cfg                        # Config spaCy pour entraînement LLM
│
└── TP-RuleBased/                         ← Méthode retenue ✅
    ├── app/
    │   ├── step2_extraction.py           # Nettoyage du corpus (800 articles)
    │   ├── step3_annotation_rulebased.py # Annotation par dictionnaire (~60 termes)
    │   ├── step4_training_ner.py         # Entraînement du modèle NER spaCy
    │   ├── step5_inference.py            # Inférence sur les 21 675 articles
    │   └── step6a_ingestion_elasticsearch.py  # Indexation dans Elasticsearch
    ├── data/
    │   ├── annotations_spacy.json        # 516 articles annotés
    │   └── data_set_nettoyé.json        # 800 articles nettoyés
    └── model_ner/                        # Modèle NER entraîné (F1 = 84.3%)
```

---

## ⚙️ Installation

### Prérequis
- Python 3.11+
- Compte [Elastic Cloud](https://cloud.elastic.co) (gratuit)
- Clé API [Groq](https://console.groq.com) (gratuite, pour TP-LLM uniquement)

### Installer les dépendances

```bash
pip install spacy groq elasticsearch python-dotenv
python -m spacy download en_core_web_sm
```

### Configurer les variables d'environnement

Crée un fichier `.env` dans chaque dossier (`TP-LLM/` et `TP-RuleBased/`) :

```env
CLOUD_ID      = "ton_cloud_id_elastic"
ES_USER       = "elastic"
ES_PASS       = "ton_mot_de_passe"
INDEX         = "tass_articles"
GROQ_API_KEY  = "ta_cle_groq"   # uniquement pour TP-LLM
```

---

## 🚀 Lancer le pipeline

### TP-RuleBased (méthode retenue ✅)

Depuis `TP-RuleBased/app/` :

```bash
# Étape 1 — Nettoyage du corpus
python step2_extraction.py

# Étape 2 — Annotation par dictionnaire
python step3_annotation_rulebased.py

# Étape 3 — Entraînement du modèle NER
python step4_training_ner.py

# Étape 4 — Inférence sur les 21 675 articles
python step5_inference.py

# Étape 5 — Indexation dans Elasticsearch
python step6a_ingestion_elasticsearch.py
```

---

### TP-LLM (méthode de comparaison)

Depuis `TP-LLM/app/` :

```bash
# Étape 1 — Nettoyage du corpus
python step2_extraction.py

# Étape 2a — Annotation Rule-Based (base de comparaison)
python step3_annotation_rulebased.py

# Étape 2b — Annotation LLM (Groq)
python step3b_annotation_llm_groq.py

# Étape 3 — Rapport comparatif
python step3c_comparaison.py

# Étape 4 — Conversion au format spaCy
python step4a_convert_spacy.py

# Étape 5 — Entraînement (via CLI spaCy)
python -m spacy train config.cfg --output ./data/output \
  --paths.train ./data/train.spacy \
  --paths.dev ./data/dev.spacy
```

---

## 📊 Résultats

### Comparaison des méthodes d'annotation

| | Rule-Based ✅ | LLM (Llama-3.1) |
|---|---|---|
| Articles annotés | **516 / 800** | 384 / 500 |
| WEAPON | 367 | 561 |
| MIL_UNIT | 254 | 600 |
| MIL_ORG | 691 | 729 |
| **TOTAL entités** | **1 312** | **1 890** |
| Termes uniques WEAPON | 43 | 424 |
| Termes uniques MIL_UNIT | 17 | 363 |
| Termes uniques MIL_ORG | 14 | 317 |
| Temps annotation | ⚡ Instantané | ⏳ 40 min |
| **F1-score modèle** | **84.3%** | 42% |

### Performances du modèle retenu (Rule-Based)

| Métrique | Score |
|---|---|
| Précision (P) | **84.3%** |
| Rappel (R) | **84.4%** |
| **F1-score** | **84.3%** |

### Insights Kibana (21 675 articles — 2015 à 2025)

| Visualisation | Insight principal |
|---|---|
| Top 10 Armes | S-400 et Kinzhal sont les plus citées |
| Top 10 Unités | Baltic Fleet domine (~410 mentions) |
| Top 10 Organisations | Rostec domine (~870 mentions) |
| Évolution temporelle | Pic en 2022-2023 (invasion Ukraine) |
| Répartition entités | MIL_ORG 56% / WEAPON 37% / MIL_UNIT 7% |

---

## 🏆 Justification du choix — Rule-Based

> Malgré un vocabulaire plus restreint (74 termes uniques vs 1 104 pour le LLM), le modèle Rule-Based atteint un **F1 de 84.3%** contre seulement **42%** pour le modèle entraîné sur les annotations LLM.
>
> Les annotations LLM introduisent du bruit (positions incorrectes, faux positifs, incohérences entre articles) qui dégrade la qualité de l'entraînement spaCy. La méthode LLM reste utile pour **enrichir le dictionnaire** Rule-Based à terme.

---

## 🛠️ Technologies

| Technologie | Usage |
|---|---|
| **spaCy 3.8** | NER, EntityRuler, entraînement, inférence |
| **Groq API (Llama-3.1-8b)** | Annotation automatique par LLM |
| **Elasticsearch** | Indexation et recherche full-text |
| **Kibana** | Dashboards de visualisation |
| **python-dotenv** | Gestion sécurisée des secrets |
| **Python 3.11** | Langage principal |

---

## ⚠️ Sécurité

Les fichiers suivants sont exclus du dépôt Git (voir `.gitignore`) :
- `.env` — contient les clés API et mots de passe
- `data/data_set.json` — corpus brut (trop volumineux)
- `data/resultats_inference.json` — résultats complets (trop volumineux)

---

## 👩‍💻 Auteur

Projet réalisé dans le cadre du cours **AI Deployment** — Eugenia School 2025/2026
