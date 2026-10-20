# Cadre de sortie d'une relecture de plan

Chaque relecteur rend sa revue dans ce cadre, et rien d'autre. Les titres, l'ordre et les
libellés de champs sont fixes : c'est ce qui permet à la synthèse d'apparier les constats de
plusieurs relecteurs et de citer chacun par son identifiant.

## Structure imposée

```markdown
## Verdict
- Décision : GO | GO-AVEC-AMENDEMENTS | NO-GO
- Résumé : ≤ 3 phrases

## Non vérifié
- <ce que tu n'as pas pu vérifier, et pourquoi : fichier non fourni, hypothèse invérifiable…>

## Constats
### <PREFIXE>-<n> — <titre court>
- Axe : intention | faisabilité | risque | périmètre | vérification | clarté
- Gravité : P1 | P2 | P3
- Section du plan : <titre exact de la section visée>
- Constat : <une phrase, falsifiable>
- Preuve : <citation du plan> + <fichier:ligne du dépôt, ou « non vérifié »>
- Si ignoré : <conséquence concrète>
- Amendement : <la modification du plan qui ferme le constat>
- Confiance : haute | moyenne | basse

## Axes sans constat
- <axe> : <en une ligne, pourquoi rien>
```

## Axes

| Axe | La question posée au plan |
|---|---|
| intention | Résout-il le problème énoncé dans son contexte ? Y a-t-il un écart entre le pourquoi et le quoi ? |
| faisabilité | Les fichiers, fonctions et outils cités existent-ils ? L'approche tient-elle contre le code réel ? Réutilise-t-elle ce qui existe déjà ? |
| risque | Régression, invariant cassé, chemin d'exécution oublié, effet de bord sur ce qui n'est pas dans le périmètre. |
| périmètre | Sur-conception, travail hors du besoin, ou pièce nécessaire absente. |
| vérification | Les critères d'acceptation sont-ils testables ? La section de vérification couvre-t-elle chaque garantie annoncée ? |
| clarté | Une ambiguïté que deux exécutants liraient différemment. |

## Gravité

- **P1** — exécuté tel quel, le plan produit un résultat faux ou casse une garantie existante.
  Bloque l'exécution.
- **P2** — le plan atteint son but, mais avec un coût, un risque ou une dette évitables. À amender
  avant d'exécuter.
- **P3** — amélioration ; n'empêche rien.

## Règles

- **Un constat par point**, falsifiable. « Le plan est flou » n'est pas un constat ; « la section
  X ne dit pas lequel des deux appelants change de signature » en est un.
- **La preuve cite** : une phrase du plan, et un `fichier:ligne` du dépôt quand le constat porte
  sur le code. Sans accès au fichier, écrire « non vérifié » — jamais deviner.
- **Douze constats au plus**, les plus graves d'abord. Un axe sur lequel tu n'as rien à dire se
  déclare dans `## Axes sans constat` ; on ne meuble pas.
- **Le préfixe d'identifiant est fourni par l'orchestrateur** (`CO-`, `CS-`, `CX-`…) et numérote
  à partir de 1. C'est ce qui rend chaque constat citable sans ambiguïté par la synthèse et par
  les amendements.
- **Le plan doit se suffire.** Tu n'as pas la conversation qui l'a produit, et c'est voulu : une
  information qui manque au plan manquera aussi à celui qui l'exécutera. Ce manque est un constat
  d'axe `clarté`.
- **L'état du disque n'est pas le plan.** Un fichier que le plan annonce créer peut être absent
  (pas encore fait) ou déjà présent (le plan a été exécuté entre sa rédaction et ta relecture) :
  ni l'un ni l'autre n'est un constat. Un écart entre le plan et le disque se note dans
  `## Non vérifié`.
- Ce cadre est la totalité de la sortie : pas de préambule, pas de conclusion hors du `Verdict`.
