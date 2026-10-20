# Gabarit du changelog hebdomadaire

Respecter cet ordre exactement :

```markdown
# Changelog — semaine du JJ au JJ mois AAAA

## En bref
- <fait marquant 1>
- <fait marquant 2>
- <fait marquant 3 (optionnel)>

## 🔒 Sécurité   ← n'afficher une section que si elle a du contenu
### <résumé ≤ 30 mots (optimum 20), sans jargon>
**Bénéfices :** <coût / risque / rendement, ancré sur la métrique de valeur de la config quand pertinent>
**Preuve de valeur :** <chiffre tracé + ce qu'il représente>   ← OU « Preuve attendue : <métrique · source · cible · quand> »
**Points d'attention :** <seulement si décision attendue, action manuelle, budget ou risque pertinent pour un non-technique ; puces si plusieurs>

## 🛡️ Fiabilité
...

## ⚡ Performance
...

## 🚀 Nouveauté
...

## Bénéfices confirmés   ← seulement si des hypothèses de semaines passées sont validées cette semaine
- <Feature (livrée sem. W) : hypothèse → résultat mesuré (chiffre + source)>

## Santé du service   ← libellé adaptable au projet (ex. « Santé du bot »)
<1-2 lignes : incidents de la semaine, correctifs déployés — depuis le registre d'incidents de la config ; omettre la section si le projet n'en a pas>

## Sous le capot
<UNE seule ligne agrégée : « Améliorations internes : tests, configuration, refactor… (N changements) »>

---
*Suivi des bénéfices non encore mesurables : `docs/changelog/value-ledger.md` (re-évalué à chaque changelog).*
```

## Exemple (générique)

Entrée technique (1 commit + son contexte) :
> `feat(jobs): reprise automatique des tâches interrompues` — un job qui plantait restait bloqué jusqu'à relance manuelle.

Bloc attendu (preuve pas encore mesurable → « Preuve attendue » + ligne au registre) :

```markdown
### 🚀 Nouveauté — Les tâches interrompues redémarrent désormais toutes seules, sans intervention.
**Bénéfices :** Moins d'interruptions de service et d'interventions manuelles.
**Preuve attendue :** zéro relance manuelle — à vérifier via <registre d'incidents · champ> la semaine prochaine.
```

Variante quand la preuve **existe déjà** :

```markdown
**Preuve de valeur :** incidents 32 → 1 en 3 jours (−97 %) — `<fichier source>`, `<champ>`.
```

Des exemples calibrés propres au projet peuvent exister dans sa config (`changelog.config.md`) — ils priment sur celui-ci.
