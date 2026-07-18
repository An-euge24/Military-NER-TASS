# 🔍 NOTE DE RENSEIGNEMENT

**Classification :** Non classifié — Usage pédagogique
**Référence :** NR-TASS-2025-001
**Date :** Juillet 2026
**Source :** Corpus TASS (2015-2025) — Analyse NLP automatisée
**Objet :** Analyse du discours militaire de l'agence TASS sur la période 2015-2025

---

## 1. RÉSUMÉ EXÉCUTIF

L'analyse automatisée de **21 675 articles** de l'agence de presse officielle
russe TASS sur dix ans révèle une **rupture majeure dans la production médiatique
militaire à partir de février 2022**, coïncidant avec l'invasion de l'Ukraine.
Le volume mensuel d'articles contenant des entités militaires a augmenté de
**plus de 350%** entre 2021 et le pic de 2023 (~550 articles/mois).

---

## 2. SYSTÈMES D'ARMES

### 2.1 Systèmes prioritairement médiatisés

Le S-400 (système de défense aérienne) constitue le système le plus cité du
corpus, reflet de son importance stratégique et diplomatique (contrat
russo-turc, tensions OTAN). Les missiles de croisière Kalibr et le missile
hypersonique Kinzhal occupent respectivement les deuxième et troisième rangs,
illustrant la communication offensive russe sur ses capacités de frappe
longue portée.

Les aéronefs Su-57 et Ka-52 concentrent l'essentiel des mentions relatives
aux plateformes aériennes, en cohérence avec leur engagement opérationnel
en Ukraine depuis 2022.

### 2.2 Évolution qualitative

Avant 2022, le discours portait principalement sur les **exportations et
démonstrations** (salons MAKS, contrats internationaux). Après février 2022,
le discours bascule vers l'**engagement opérationnel** et les performances
au combat.

---

## 3. ACTEURS INSTITUTIONNELS

### 3.1 Acteurs russes

**Rostec** (conglomérat d'armement d'État) domine avec ~870 mentions, confirmant
son rôle central dans la communication officielle russe sur la défense. Le
**Ministère de la Défense** (~820 mentions) constitue la source institutionnelle
principale des communiqués repris par TASS.

### 3.2 Acteurs adversaires et alliés

**NATO/OTAN** apparaît dans ~650 articles, systématiquement positionnée comme
menace dans le cadre narratif de TASS. Cette présence élevée reflète la
construction rhétorique de la justification de l'intervention militaire russe.

---

## 4. UNITÉS OPÉRATIONNELLES

La **Flotte de la Baltique** (~410 mentions) et la **Flotte de la Mer Noire**
(~310 mentions) dominent les citations d'unités, traduisant les tensions
maritimes persistantes avec l'OTAN en mer Baltique et les opérations en
mer Noire depuis l'annexion de la Crimée (2014).

Les **Forces aérospatiales** enregistrent une forte progression après 2022,
cohérente avec l'intensité des opérations aériennes en Ukraine.

---

## 5. ANALYSE TEMPORELLE

| Période | Signal | Interprétation |
|---|---|---|
| 2015-2016 | Hausse modérée | Engagement en Syrie |
| 2019-2020 | Stabilisation | Période de consolidation |
| 2021 | Creux | Possible période de préparation |
| Fév. 2022 | Rupture majeure | Invasion de l'Ukraine |
| 2023 | Pic maximum (~550/mois) | Intensification du conflit |
| 2024-2025 | Décroissance progressive | Routinisation du discours |

---

## 6. LIMITES DE L'ANALYSE

- **Biais de source :** TASS est l'agence officielle russe — le corpus reflète
  le discours d'État et non la réalité opérationnelle.
- **Langue unique :** Seuls les articles en anglais ont été analysés,
  excluant le corpus russophone plus volumineux.
- **NER partiel :** Le modèle Rule-Based couvre ~60 termes prédéfinis ;
  des entités inconnues peuvent avoir été manquées.
- **Absence de vérification terrain :** Les entités détectées reflètent
  la médiatisation et non la réalité des engagements.

---

## 7. CONCLUSION

Le corpus TASS constitue un **indicateur fiable de la communication stratégique
russe** sur les questions militaires. L'analyse NLP automatisée permet d'en
extraire des signaux structurés à grande échelle, impossibles à traiter
manuellement. La corrélation entre les pics de mentions et les événements
géopolitiques majeurs valide la pertinence de l'approche.

Cette méthode, appliquée en temps réel et étendue à d'autres sources
(agences occidentales, réseaux sociaux), constituerait un outil d'analyse
OSINT opérationnel.

---

**Rédigé par :** Andréa SALEMO
**Dans le cadre de :** Cours AI Deployment — Eugenia School 2025/2026
**Outils utilisés :** spaCy NER, Elasticsearch, Kibana, Python 3.11
