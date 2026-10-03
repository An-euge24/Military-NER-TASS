# Démonstration Elasticsearch locale

Cette configuration est destinée à la démonstration et aux captures de la soutenance. Elle ne constitue pas un déploiement de production : la sécurité Elasticsearch est désactivée uniquement sur la machine locale.

## Démarrage

Depuis le dossier contenant `docker-compose.elasticsearch.yml` :

```powershell
docker compose -f deployment/docker-compose.elasticsearch.yml up -d
```

Vérifier Elasticsearch :

```powershell
Invoke-RestMethod http://localhost:9200
Invoke-RestMethod http://localhost:9200/_cluster/health
```

Ouvrir Kibana dans le navigateur :

```text
http://localhost:5601
```

## Indexation

Créer un fichier `.env` local à partir de `.env.example`, sans le versionner :

```dotenv
ES_URL=http://localhost:9200
INDEX=tass_articles_soutenance_2026
RESET_INDEX=false
```

Puis lancer le script local :

```powershell
python step6a_ingestion_elasticsearch_local.py
```

Le script utilise `resultats_inference.json`, crée l’index avec un mapping explicite et indexe les documents par lots. Pour éviter une suppression accidentelle, `RESET_INDEX=false` est la valeur par défaut.

## Captures recommandées

1. Les conteneurs Elasticsearch et Kibana actifs.
2. La réponse `/_cluster/health`.
3. La création de l’index `tass_articles_soutenance_2026`.
4. Le nombre de documents indexés.
5. Une requête de recherche sur les armes ou organisations.
6. Un dashboard Kibana avec la période du 7 juillet 2016 au 7 juillet 2026.

## Arrêt et nettoyage

```powershell
docker compose -f deployment/docker-compose.elasticsearch.yml down
```

Pour supprimer également les données locales de démonstration :

```powershell
docker compose -f deployment/docker-compose.elasticsearch.yml down -v
```
