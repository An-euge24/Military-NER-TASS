# Scripts pipeline avec logs détaillés

Ces fichiers remplacent les scripts correspondants du projet. Ils ne contiennent ni données, ni modèle, ni `.env` réel.

Chaque étape journalise les volumes, les durées, les sorties et les erreurs utiles.

## Fichiers

- `step2_extraction_logged.py` : corpus lu, articles valides, échantillon et taille de sortie ;
- `step3_annotation_rulebased_logged.py` : chargement spaCy, articles annotés, labels, articles ignorés et durée ;
- `step4_training_ner_logged.py` : train, validation, précision, rappel, F1-score, durée et dossier modèle ;
- `step5_inference_logged.py` : modèle, corpus, progression, débit, entités et JSON ;
- `step6a_ingestion_elasticsearch_local_logged.py` : connexion, lots, documents, erreurs, refresh et durée.

Les fichiers JSON de métriques sont écrits dans `logs/`.
