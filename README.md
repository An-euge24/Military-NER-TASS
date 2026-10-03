# Military-NER-TASS

## Présentation

Military-NER-TASS est un prototype de veille documentaire et d'extraction automatique d'entités militaires.

Le projet analyse des articles publics du corpus TASS et identifie trois catégories d'entités :

- `WEAPON` : armes et systèmes d'armement ;
- `MIL_UNIT` : unités, groupes et formations militaires ;
- `MIL_ORG` : organisations, ministères et alliances militaires.

L'objectif est d'aider un analyste à retrouver rapidement les informations importantes dans un grand volume d'articles. Le projet ne remplace pas une analyse humaine et ne constitue pas un outil de décision opérationnelle.

## Fonctionnement général

```text
Articles TASS
    ↓
Extraction et nettoyage
    ↓
Annotation LLM exploratoire et annotation rule-based
    ↓
Entraînement du modèle NER spaCy
    ↓
Inférence sur les articles
    ↓
Résultats JSON
    ↓
Elasticsearch et Kibana
    ↓
API Docker de prédiction
```

Deux méthodes d'annotation ont été étudiées. La méthode LLM a été utilisée comme méthode exploratoire et de pré-annotation. La méthode rule-based a été retenue pour la production, car elle était plus homogène, reproductible et performante dans l'expérimentation du projet.

## Résultats principaux

L'inférence complète a traité :

- 21 675 articles valides ;
- 13 648 articles avec au moins une entité ;
- 8 027 articles sans entité ;
- 34 848 entités détectées.

Répartition des entités détectées :

- `MIL_ORG` : 18 612 ;
- `WEAPON` : 9 266 ;
- `MIL_UNIT` : 6 970.

Résultats du réentraînement local sur le jeu de validation utilisé :

- précision : 94,40 % ;
- rappel : 96,56 % ;
- F1-score : 95,47 %.

## Organisation du projet

```text
Military-NER-TASS/
├── TP - Rule Based/
│   ├── app/
│   │   ├── step2_extraction.py
│   │   ├── step3_annotation_rulebased.py
│   │   ├── step3b_annotation_llm_groq.py
│   │   ├── step4_training_ner.py
│   │   └── step5_inference.py
│   ├── data/
│   ├── model_ner/
│   ├── deployment/
│   ├── Bloc4/
│   ├── logs/
│   ├── tests/
│   └── step6a_ingestion_elasticsearch_local.py
├── TP - LLM/
└── README.md
```

## Installation sous Windows

Depuis le dossier `TP - Rule Based` :

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Le modèle final entraîné doit être présent dans :

```text
model_ner/
```

## Tests

Depuis la racine de `TP - Rule Based` :

```powershell
python -m pytest -q
```

Résultat attendu :

```text
2 passed
```

## Exécution du pipeline

Les étapes peuvent être exécutées séparément :

```powershell
python .\app\step2_extraction.py
python .\app\step3_annotation_rulebased.py
python .\app\step4_training_ner.py
python .\app\step5_inference.py
python .\step6a_ingestion_elasticsearch_local.py
```

Attention :

- l'entraînement remplace le contenu de `model_ner/` ;
- l'inférence complète peut prendre plusieurs minutes ;
- l'indexation doit être lancée après la création de `resultats_inference.json` ;
- les métriques sont conservées dans `logs/`.

## Elasticsearch et Kibana

Démarrer l'infrastructure locale :

```powershell
docker compose -f .\deployment\docker-compose.elasticsearch.yml up -d
```

Vérifier Elasticsearch :

```powershell
Invoke-RestMethod http://localhost:9200
Invoke-RestMethod http://localhost:9200/_cluster/health
```

Kibana est disponible à l'adresse :

```text
http://localhost:5601
```

L'index utilisé pour la démonstration est :

```text
tass_articles_soutenance_2026
```

## API du Bloc 4

Installer les dépendances de l'API :

```powershell
python -m pip install -r .\Bloc4\02_Code_Developpement\requirements.txt
```

Démarrer l'API :

```powershell
Set-Location .\Bloc4\03_Code_Deployement
python -m uvicorn api:app --reload --port 8000
```

Documentation interactive :

```text
http://127.0.0.1:8000/docs
```

Endpoints disponibles :

- `GET /health` : vérifie que le modèle est chargé ;
- `POST /predict` : extrait les entités d'un texte ;
- `GET /metrics` : affiche les métriques simples du service.

Le service peut également être démarré avec Docker :

```powershell
docker compose -f .\Bloc4\03_Code_Deployement\docker-compose.yml up --build
```

## Sécurité

Les fichiers suivants ne doivent jamais être publiés :

```text
.env
.env.local
*.key
*.pem
```

Le dépôt peut contenir uniquement :

```text
.env.example
```

Les clés Groq, mots de passe Elasticsearch, Cloud ID et clés API doivent rester dans des variables d'environnement locales.

## Limites

- Le modèle est spécialisé sur le corpus TASS et le domaine militaire étudié ;
- les annotations automatiques ne constituent pas une vérité terrain exhaustive ;
- certaines entités peuvent être manquées ou mal classées ;
- une validation humaine reste nécessaire ;
- l'infrastructure locale Elasticsearch/Kibana est destinée à la démonstration et n'est pas une architecture haute disponibilité ;
- les dashboards doivent toujours être interprétés avec leur période et leur filtre temporel.

## Licence et usage

Projet réalisé dans le cadre d'une soutenance. Les sources et données utilisées doivent respecter les conditions d'utilisation applicables au corpus TASS.
