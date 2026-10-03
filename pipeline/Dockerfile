# Image Python légère adaptée à l'exécution du pipeline.
FROM python:3.11-slim

# Évite les fichiers .pyc et force l'affichage immédiat des logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Tous les chemins du conteneur partent de ce répertoire.
WORKDIR /project

# Installation des dépendances avant la copie du code,
# afin de pouvoir réutiliser le cache Docker si le code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des trois éléments nécessaires à l'inférence.
COPY app ./app
COPY data ./data
COPY model_ner ./model_ner

# Le script actuel utilise des chemins relatifs depuis le dossier app.
WORKDIR /project/app

# Commande exécutée au démarrage du conteneur.
CMD ["python", "step5_inference.py"]
