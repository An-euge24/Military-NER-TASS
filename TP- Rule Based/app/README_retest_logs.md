# Retest de production avec logs de temps

Pour obtenir des captures plus utiles, utiliser les scripts instrumentés :

- `step5_inference_logged.py` : chargement du modèle, chargement des données, durée d’inférence, débit et taille du JSON ;
- `step6a_ingestion_elasticsearch_local_logged.py` : temps de connexion, temps d’indexation, temps total, erreurs et comptage final.

La limite actuelle de 1 000 caractères est affichée explicitement dans les logs afin de rester cohérente avec les résultats déjà produits.

## Séquence recommandée

1. Lancer l’inférence instrumentée depuis le dossier `app`.
2. Capturer les logs de chargement et les métriques finales.
3. Lancer l’indexation locale instrumentée.
4. Capturer le temps d’indexation et le comptage final.
5. Actualiser l’index puis vérifier `21675` documents dans Kibana.

Il n’est pas nécessaire de refaire l’entraînement du modèle pour ce retest.
