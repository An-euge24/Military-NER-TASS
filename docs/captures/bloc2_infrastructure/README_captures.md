# Captures de production, Bloc 2

Les captures sont sélectionnées pour démontrer l’exécution réelle de l’infrastructure :

1. Docker démarre Elasticsearch et Kibana.
2. Elasticsearch est en état `green`.
3. 21 675 documents sont indexés sans erreur après actualisation de l’index.
4. La Data View Kibana utilise l’index `tass_articles_soutenance_2026` et le champ `date`.
5. Discover permet de consulter les champs `title`, `mil_orgs`, `mil_units`, `weapons` et `nb_entities`.
