# Livrable Bloc 4, solution IA et déploiement

Le Bloc 4 présente la transformation du modèle NER en solution IA exploitable.

- `01_Presentation/` : présentation de 5 minutes et plan des slides ;
- `02_Code_Developpement/` : prédiction, réentraînement, dérive et tests ;
- `03_Code_Deployement/` : API FastAPI, Dockerfile et Docker Compose ;
- `04_Captures_Production/` : captures à réaliser lors du lancement local ;
- `05_Documentation/` : guide d'utilisation, model card et procédure de réentraînement.

La méthode rule-based est la méthode retenue pour la solution finale. L'expérimentation LLM est documentée dans le Bloc 3, mais n'est pas une dépendance du service de production.

Le dossier `model_ner/` doit rester à la racine du projet. Les secrets ne sont jamais inclus dans le livrable.
