# Config changelog hebdomadaire — <NOM DU PROJET>

> Config projet du skill `changelog-hebdo`. Instanciée par le setup, maintenue à la main.
> Règle : chaque source cite des chemins et champs réels du dépôt — pas de généralités.

## Audience

- Lecteurs : <rôles, niveau technique, langue>.
- <Contraintes de lecture particulières, s'il y en a.>

## Contexte produit

- <Ce que fait le produit, en 1-2 phrases orientées valeur.>
- **Métrique de valeur** : <formule ou axe (revenu / coût / risque…)> — ancrer les bénéfices dessus.
- Idées reçues à ne PAS signaler comme anomalies : <ex. « comportement X est voulu par design ».>
- Références de ton/vocabulaire : <fichiers à consulter, ex. README, doc métier.>

## Sources

- **Changements** : `git log --since='<fenêtre>' --pretty=format:'%h %ad %s' --date=short --no-merges` — <conventions observées : format, langue, types/scopes>.
- **Pourquoi métier** : <chemin des docs de contexte (dev-notes, ADR, PR…) et comment filtrer par fenêtre>.
- **Incidents** : <chemin du registre de problèmes / post-mortems, ou « aucun »>.
- **Preuves chiffrées** (fichier · champs exacts · disponibilité) :
  - <source 1 — versionnée ou runtime ?>
  - <source 2…>

## Glossaire (jargon → traduction lecteur)

- <terme technique> = <traduction en ≤ 4 mots>
- …

## Surcharges de mapping (optionnel)

- <ex. scope `resilience` → Fiabilité ; type custom → catégorie.>

## Sortie

- Dossier : <défaut `docs/changelog/`> ; fichiers `YYYY-Www.md` + `value-ledger.md`.

## Exemples calibrés (optionnel)

<1-2 blocs de changelog réels du projet, pour caler le style d'une exécution à l'autre.>
