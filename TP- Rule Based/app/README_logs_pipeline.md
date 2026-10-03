# Logs et métriques du pipeline

Les scripts du pipeline conservent leurs noms fonctionnels : `step2_extraction.py`, `step3_annotation_rulebased.py`, `step4_training_ner.py`, `step5_inference.py` et `step6a_ingestion_elasticsearch_local.py`.

Les logs détaillés sont intégrés directement dans les scripts. Ils indiquent notamment les volumes traités, les durées, les sorties produites, les entités détectées, les erreurs éventuelles et le débit d’exécution.

Le fichier `run_pipeline.py` ajoute :

- une heure de début et de fin pour chaque étape ;
- la durée de chaque étape ;
- le code retour ;
- la conservation de la sortie standard et des erreurs dans un fichier `.log` ;
- un fichier `pipeline_metrics.json` avec les volumes, les entités et les tailles de fichiers.

## Exemples

Lancer les étapes sans refaire l’entraînement :

```powershell
python run_pipeline.py --from-step step5 --to-step step6a
```

Lancer le pipeline complet, y compris l’entraînement :

```powershell
python run_pipeline.py
```

Le pipeline complet n’a pas besoin d’être relancé pour la soutenance si les résultats et les logs d’exécution existants sont déjà conservés.
