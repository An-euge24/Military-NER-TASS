# Captures de production, Bloc 3

Les captures montrent le pipeline jusqu’à la restitution :

1. lancement de l’indexation avec 21 675 articles chargés, 21 675 documents indexés et zéro erreur ;
2. actualisation puis comptage final de 21 675 documents dans Elasticsearch ;
3. consultation des résultats dans Kibana Discover ;
4. état green du cluster utilisé pour la restitution.

Le premier comptage affiché avant actualisation était temporairement inférieur. La capture de comptage final après `_refresh` est la preuve de référence.

5. `05_Metriques_inference_JSON.png` : métriques structurées, débit de 18,09 articles/s et taille du JSON.
6. `06_Indexation_retest_logs_temps.png` : retest avec 21 675 documents, zéro erreur et durée d’indexation de 2,55 s.
7. `07_Inference_complete_logs.png` : progression et métriques finales de l’inférence complète.
8. `08_Tests_smoke_2_passed.png` : vérification des tests du projet.
