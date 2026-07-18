# 📊 Analyse des métriques et choix des dashboards

## 1. Contexte

Le dashboard **"Analyse Militaire TASS"** a été conçu pour explorer les résultats
de l'inférence NER sur **21 675 articles TASS** (2015-2025). Cinq visualisations
ont été sélectionnées pour couvrir trois axes analytiques : les acteurs, les
équipements et la temporalité.

---

## 2. Analyse des visualisations

### 📊 Visualisation 1 — Top 10 des armes citées (Bar chart horizontal)

**Choix justifié par :**
- Permet d'identifier rapidement les **systèmes d'armes les plus médiatisés**
- Le graphique horizontal facilite la lecture des labels (noms longs)
- Le tri décroissant met en évidence la hiérarchie des mentions

**Métriques clés :**
| Arme | Mentions |
|---|---|
| S-400 | ~230 |
| Kinzhal | ~180 |
| Ka-52 | ~160 |
| Kalibr | ~150 |
| Su-57 | ~140 |

**Interprétation :**
Le S-400 domine car il est au cœur des négociations diplomatiques russo-turques
et de la stratégie de défense aérienne russe. Le Kinzhal (missile hypersonique)
reflète la communication offensive de la Russie sur ses capacités stratégiques
depuis 2022.

---

### 📊 Visualisation 2 — Top 10 des unités militaires (Bar chart horizontal)

**Choix justifié par :**
- Permet d'identifier les **théâtres d'opération prioritaires** via les unités les
  plus citées
- Révèle la répartition géographique des opérations (mer, air, terre)

**Métriques clés :**
| Unité | Mentions |
|---|---|
| Baltic Fleet | ~410 |
| Aerospace Forces | ~380 |
| Black Sea Fleet | ~310 |
| Battlegroup East | ~280 |

**Interprétation :**
La Baltic Fleet et la Black Sea Fleet reflètent les tensions maritimes avec l'OTAN.
Les Aerospace Forces dominent depuis février 2022 avec l'intensification des frappes
aériennes sur l'Ukraine.

---

### 📊 Visualisation 3 — Top 10 des organisations militaires (Bar chart horizontal)

**Choix justifié par :**
- Identifie les **acteurs institutionnels** dominants dans le discours TASS
- Distingue acteurs russes, ukrainiens et internationaux

**Métriques clés :**
| Organisation | Mentions |
|---|---|
| Rostec | ~870 |
| Defense Ministry | ~820 |
| NATO | ~650 |
| Russian Defense Ministry | ~580 |

**Interprétation :**
Rostec (conglomérat d'armement d'État) domine car TASS couvre intensément
la production et l'exportation d'armements russes. La forte présence de NATO
révèle que TASS positionne systématiquement l'alliance comme adversaire rhétorique.

---

### 📊 Visualisation 4 — Évolution temporelle (Line chart)

**Choix justifié par :**
- Visualisation **indispensable** pour corréler la production médiatique aux
  événements géopolitiques
- Le line chart est le format le plus lisible pour une série temporelle continue
- Intervalle mensuel : granularité optimale sur 10 ans

**Métriques clés :**
| Période | Articles/mois | Événement |
|---|---|---|
| 2016-2020 | ~100-200 | Activité de base |
| 2021 | ~70 | Creux (Covid, réduction éditoriale) |
| Fév. 2022 | +350% | Invasion de l'Ukraine |
| Pic 2023 | ~550 | Maximum absolu |
| 2024-2025 | ~150-370 | Baisse progressive |

**Interprétation :**
L'explosion de 2022-2023 constitue une **preuve de validité du modèle NER** :
le pipeline capture fidèlement la réalité du conflit dans les données médiatiques.
Le creux de 2021 précède l'invasion et pourrait refléter une période de
préparation moins médiatisée.

---

### 📊 Visualisation 5 — Répartition WEAPON / MIL_UNIT / MIL_ORG (Donut chart)

**Choix justifié par :**
- Le donut chart est optimal pour visualiser une **répartition en 3 catégories**
- Donne une vue synthétique de la nature du discours militaire de TASS

**Métriques clés :**
| Catégorie | Part |
|---|---|
| MIL_ORG | ~56% |
| WEAPON | ~37% |
| MIL_UNIT | ~7% |

**Interprétation :**
La dominance des MIL_ORG (56%) révèle que TASS privilégie un discours
**institutionnel et diplomatique** plutôt qu'opérationnel. Les armes (37%)
reflètent la communication sur les capacités militaires. Les unités (7%)
sont peu citées nominalement, TASS préférant les références génériques
("les forces armées", "l'armée").

---

## 3. Cohérence globale des choix

| Axe analytique | Visualisation | Apport |
|---|---|---|
| **Équipements** | Top 10 Armes | Quels systèmes sont mis en avant ? |
| **Acteurs** | Top 10 Unités + Organisations | Qui sont les protagonistes ? |
| **Temporalité** | Évolution temporelle | Quand et comment le discours évolue-t-il ? |
| **Synthèse** | Répartition entités | Quelle est la nature du discours ? |

Les 5 visualisations sont **complémentaires** : elles répondent aux questions
Qui ? Quoi ? Quand ? et Comment ? — les quatre piliers de l'analyse de
renseignement ouverte (OSINT).
