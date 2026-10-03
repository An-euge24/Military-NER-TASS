# Model card, Military-NER-TASS

## Usage

Extraction d'entités militaires dans des articles du corpus TASS.

## Labels

`WEAPON`, `MIL_UNIT`, `MIL_ORG`.

## Données

Le modèle est entraîné sur des annotations rule-based validées dans le cadre du projet. La limite documentaire utilisée dans l'expérimentation est documentée dans les plans et les logs.

## Résultats

Le réentraînement local documenté affiche une précision de 94,40 %, un rappel de 96,56 % et un F1-score de 95,47 % sur le jeu de validation utilisé.

## Limites

Le modèle dépend du vocabulaire du corpus TASS et peut produire des erreurs sur des textes hors domaine. Les résultats doivent être contrôlés avant une utilisation opérationnelle.
