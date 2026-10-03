# Bloc 4, solution IA et déploiement

## Objectif

Transformer le modèle NER rule-based entraîné dans le projet en une solution IA utilisable, testable, déployable et maintenable.

## Pré-requis

Le dossier `model_ner/` doit rester à la racine du projet, au même niveau que `Bloc4/`.

## Lancement local de l'API

Depuis la racine du projet :

```powershell
python -m pip install -r .\Bloc4\02_Code_Developpement\requirements.txt
Set-Location .\Bloc4\03_Code_Deployement
uvicorn api:app --reload --port 8000
```

Endpoints :

- `GET http://localhost:8000/health`
- `POST http://localhost:8000/predict`
- `GET http://localhost:8000/metrics`

Exemple de requête PowerShell :

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/predict `
  -Method Post `
  -ContentType 'application/json' `
  -Body '{"text":"Russia deployed the S-400 system near the military base."}'
```

## Déploiement Docker

Depuis la racine du projet :

```powershell
docker compose -f .\Bloc4\03_Code_Deployement\docker-compose.yml up --build
```

Le service est disponible sur le port `8000`.

## Sécurité

Ne jamais inclure `.env`, les clés API, les mots de passe ou les identifiants dans l'archive finale. Seul `.env.example` peut être remis.
