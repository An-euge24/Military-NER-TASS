# Military-NER-TASS

Projet de veille documentaire et d'extraction automatique d'entités militaires dans des articles publics du corpus TASS.

Le système identifie trois catégories d'entités :

- `WEAPON` : armes et systèmes d'armes ;
- `MIL_UNIT` : unités militaires ;
- `MIL_ORG` : organisations militaires.

## Vue d'ensemble

```text
Articles TASS
    ↓
Extraction et nettoyage
    ↓
Annotation rule-based ou LLM exploratoire
    ↓
Entraînement du modèle NER spaCy
    ↓
Inférence
    ↓
JSON et métriques
    ↓
Elasticsearch et Kibana
    ↓
API FastAPI et Docker
```

## Organisation du dépôt

```text
Military-NER-TASS/
├── TP - LLM/
│   └── Expérimentation de l'annotation par LLM et comparaison historique
├── TP- Rule Based/
│   └── Projet de référence avec données, modèle et code historique
├── pipeline/
│   ├── app/
│   ├── deployment/
│   └── tests/
├── solution_ia/
│   ├── api.py
│   ├── predict.py
│   ├── detect_drift.py
│   ├── retrain_model.py
│   ├── Dockerfile
│   └── tests/
├── docs/
│   └── captures/
│       ├── bloc2_infrastructure/
│       ├── bloc3_pipeline/
│       └── bloc4_solution_ia/
└── README.md
```

Les dossiers `pipeline/` et `solution_ia/` correspondent à l'organisation technique finale. Les dossiers `TP - LLM/` et `TP- Rule Based/` conservent les travaux expérimentaux et historiques.

## Méthodes d'annotation

Deux approches ont été étudiées :

| Approche | Principe | Résultat historique |
|---|---|---:|
| LLM | Pré-annotation par modèle de langage | F1-score d'environ 42 % |
| Rule-based | Dictionnaire et `EntityRuler` spaCy | F1-score d'environ 84,3 % |

La méthode rule-based a été retenue pour la production, car elle est plus homogène, reproductible, explicable et adaptée aux contraintes du projet.

## Résultats principaux

L'inférence complète de référence a traité :

- 21 675 articles valides ;
- 13 648 articles contenant au moins une entité ;
- 34 848 entités détectées ;
- 18 612 `MIL_ORG` ;
- 9 266 `WEAPON` ;
- 6 970 `MIL_UNIT`.

Un réentraînement local distinct, réalisé sur 412 articles d'entraînement et 104 articles de validation, a obtenu :

- précision : 94,40 % ;
- rappel : 96,56 % ;
- F1-score : 95,47 %.

Ces métriques de réentraînement ne doivent pas être confondues avec les résultats historiques de comparaison des méthodes ni avec les métriques de l'inférence complète.

## Pipeline final

Le dossier `pipeline/` contient :

- l'extraction et le nettoyage des articles ;
- l'annotation rule-based ;
- l'entraînement spaCy ;
- l'inférence ;
- l'indexation locale dans Elasticsearch ;
- les métriques du pipeline ;
- les tests smoke.

Les instructions détaillées se trouvent dans les fichiers README du dossier `pipeline/`.

## Solution IA et déploiement

Le dossier `solution_ia/` contient :

- une fonction de prédiction ;
- une API FastAPI avec les endpoints `/health`, `/predict` et `/metrics` ;
- une détection simple de dérive ;
- un script de réentraînement ;
- des tests automatisés ;
- un `Dockerfile` et un fichier `docker-compose.yml`.

La solution a été vérifiée en exécution locale et dans Docker. Les captures correspondantes sont disponibles dans `docs/captures/bloc4_solution_ia/`.

## Elasticsearch et Kibana

Les résultats d'inférence peuvent être indexés dans Elasticsearch puis consultés dans Kibana. Les preuves techniques sont disponibles dans :

- `docs/captures/bloc2_infrastructure/` ;
- `docs/captures/bloc3_pipeline/`.

## Installation générale

Créer un environnement virtuel, puis installer les dépendances nécessaires :

````bash
python -m venv .venv
.venv\Scripts\activate
pip install -r pipeline/requirements.txt
````

Pour l'API, consulter `solution_ia/README_Bloc4.md` et utiliser le fichier `solution_ia/.env.example` comme modèle de configuration.

## Sécurité

Ne jamais versionner :

- un fichier `.env` réel ;
- une clé Groq ou une autre clé API ;
- un mot de passe Elasticsearch ;
- un identifiant Cloud Elastic ;
- des secrets présents dans les captures d'écran.

Seuls les fichiers `.env.example` sont conservés dans le dépôt.

## Limites

Les annotations automatiques nécessitent une supervision humaine. Les performances dépendent du dictionnaire utilisé, du domaine documentaire et de la qualité des données d'entraînement. Le modèle aide l'analyste, mais ne remplace pas son expertise.

## Livrables de soutenance

Les documents Word, PDF et présentations de soutenance sont conservés séparément. Ils ne font pas partie de ce dépôt technique.
