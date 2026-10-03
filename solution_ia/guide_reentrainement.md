# Guide de réentraînement

1. Collecter de nouveaux articles.
2. Anonymiser et contrôler la source.
3. Annoter avec la méthode rule-based.
4. Valider un échantillon humainement.
5. Comparer la distribution des catégories avec le corpus de référence.
6. Si une dérive est détectée, lancer `retrain_model.py`.
7. Évaluer précision, rappel et F1-score.
8. Remplacer le modèle uniquement si les résultats sont validés.
9. Conserver les métriques et la version du modèle.
