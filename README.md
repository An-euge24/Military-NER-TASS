# Military-NER-TASS

Projet de veille documentaire et d'extraction automatique d'entités militaires dans des articles publics du corpus TASS.

Le projet identifie trois catégories :

- `WEAPON` : armes et systèmes d'armes ;
- `MIL_UNIT` : unités militaires ;
- `MIL_ORG` : organisations militaires.

## Organisation

- `pipeline/` : extraction, annotation rule-based, entraînement, inférence et ingestion Elasticsearch ;
- `solution_ia/` : prédiction, détection de dérive, réentraînement et API FastAPI/Docker ;
- `docs/captures/` : preuves techniques des Blocs 2, 3 et 4.

Les documents PDF, Word et présentations de soutenance ne sont pas inclus dans ce dépôt. Ils sont conservés séparément dans les livrables de soutenance.

## Sécurité

Ne jamais versionner un fichier `.env` réel, une clé API ou un mot de passe. Utiliser les fichiers `.env.example` comme modèles et renseigner les secrets uniquement en local.
