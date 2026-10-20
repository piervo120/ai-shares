---
name: changelog-hebdo
description: "Changelog hebdomadaire orienté décideurs non techniques : commits + docs du projet traduits en valeur métier, preuves chiffrées traçables, registre de valeur suivi dans le temps. Pour toute demande de changelog ou rapport hebdomadaire des évolutions. Auto-setup au premier lancement."
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Changelog hebdomadaire (décideurs)

Traduire les changements techniques de la semaine en valeur métier pour lecteurs non techniques. Skill générique : tout le contexte projet vit dans une config par dépôt.

## Configuration projet (obligatoire)

Lire `docs/changelog/changelog.config.md`. **Absente → dérouler `references/setup.md`** (setup guidé qui explore le dépôt, pose les questions nécessaires et écrit la config), puis continuer.

La config fournit : contexte produit + métrique de valeur, sources (commits, docs de contexte, incidents, preuves chiffrées avec champs exacts), glossaire de traduction du jargon, surcharges de mapping, emplacement de sortie. Ne jamais deviner un élément que la config devrait fournir — compléter la config d'abord.

## Invariants (quel que soit le projet)

- Lecture < 2 min ; phrases courtes, pas de paragraphes ; zéro jargon non traduit (via le glossaire de la config).
- Ton neutre (pas de superlatifs) ; chiffre brut à côté de tout signal qualitatif.
- Bénéfices ancrés sur la métrique de valeur du projet (coût / risque / rendement).
- Fenêtre par défaut : 7 derniers jours ; accepter une plage ou une liste de commits en argument.
- Mapping fermé type de commit → catégorie (la config peut le surcharger) :
  - `feat` → 🚀 Nouveauté · `fix` → 🛡️ Fiabilité · `perf` → ⚡ Performance · `security` (ou `fix` à impact sécurité) → 🔒 Sécurité
  - `chore` / `test` / `refactor` / `style` / `docs` / `ci` / `build` → 🔧 Sous le capot : **une seule ligne agrégée**, pas de bloc.
- Ordre des sections : Sécurité > Fiabilité > Performance > Nouveauté — jamais chronologique. Une entrée par feature (regrouper les commits liés).

## Preuve de valeur

Ligne obligatoire sur chaque évolution visible, dans un des trois états :

1. **Mesurée** — chiffre brut + ce qu'il représente + source exacte (fichier · champ/date). Pas de source → pas de chiffre ; aucune estimation ni ordre de grandeur inventé.
2. **Attendue** — pas encore de mesure : documenter effet attendu, métrique exacte (fichier · champ), cible/sens, quand évaluer → ajouter au registre.
3. **Qualitative** — ni mesure ni métrique surveillable : rester factuel sur l'effet observable, sans extrapoler.

Source de preuve indisponible (rapport non généré…) → dégrader en « attendue » (nommer le champ à mesurer), ne jamais fabriquer la donnée.

### Registre de valeur — `<dossier de sortie>/value-ledger.md`

Persistant, versionné. Colonnes fixes :
`| Feature | Semaine livrée | Hypothèse de valeur | Métrique & source (fichier · champ) | Cible / sens | Statut | Preuve mesurée | Évalué le |`
avec `Statut` ∈ `en-attente` · `confirmé` · `infirmé` · `abandonné`.

À chaque génération :
1. Lire le registre (le créer s'il n'existe pas).
2. Nouvelles évolutions sans preuve mesurable → ligne `en-attente`.
3. Lignes `en-attente` passées → re-mesurer : donnée disponible → `confirmé`/`infirmé` + `Preuve mesurée` + `Évalué le`, et remonter dans « Bénéfices confirmés » du changelog ; sinon laisser `en-attente`.

## Sortie

Écrire `<dossier de sortie>/YYYY-Www.md` (dossier défini par la config, défaut `docs/changelog/`) en suivant `references/gabarit.md`. En cas de doute sur l'emplacement, demander avant d'écrire.
