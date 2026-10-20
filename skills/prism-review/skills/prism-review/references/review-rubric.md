# Grille de revue

Commune aux trois voix de `prism-review`. Chaque relecteur la lit et rend ses constats dans ce
format ; la synthèse ne peut apparier que des constats rendus de la même façon.

## Marquage

- **[P1]** — défaut réel : on peut nommer une entrée concrète ou une séquence d'appels qui
  produit une sortie fausse, une perte de données, une faille ou un blocage.
- **[P2]** — fragilité, écart de contrat ou de convention sans entrée fautive démontrable.

Chaque constat porte `fichier:ligne`. Un constat sans ligne est invérifiable, donc écarté.

## Axes, par ordre de priorité

1. **Fidélité au contrat.** L'implémentation tient-elle ce que le brief ou le plan promet ?
   Chercher les chemins d'exécution que la promesse exclut et que le code autorise. La voix
   aveugle, qui n'a ni brief ni plan, n'applique pas cet axe : « Axe 1 : sans objet ».
2. **Contrat écrit contre code.** Documentation, README, commentaires de contrat, messages
   d'erreur : disent-ils ce que le code fait vraiment ?
3. **Invariants sur séquences tordues.** Appels dans le désordre, répétés, interrompus à
   mi-chemin ; entrées vides, extrêmes, dupliquées ; concurrence si le code en a.
4. **Ce que les tests ne couvrent pas.** Un chemin modifié sans test qui le franchit, une
   assertion trop lâche pour échouer, un test qui reproduit l'implémentation au lieu de la
   contraindre.
5. **Sécurité de base.** Entrée non validée aux frontières, secret en clair, injection,
   autorisation absente, donnée sensible journalisée.
6. **Sur-complexité.** Abstraction à usage unique, option que personne n'a demandée, code mort
   introduit par le lot.

Les conventions que le dépôt déclare (`CLAUDE.md`, `AGENTS.md`, configuration de lint) priment sur
tout idiome générique.

## Forme du rendu

Un titre par axe qui a donné quelque chose, puis la liste des constats :

```
[P1] chemin/fichier.ext:42 — <défaut en une phrase>
     Entrée / séquence : <le cas concret>
     Effet : <sortie fausse ou dommage>

[P2] chemin/fichier.ext:42 — <fragilité ou écart en une phrase>
     Pourquoi : <ce qui l'expose, ou le contrat écrit qu'elle contredit>
```

Un [P2] n'a pas d'entrée fautive démontrable : ne pas en inventer, ne pas laisser de champ vide.

Un axe qui ne donne rien se dit en une ligne (« Axe 4 : rien à signaler »). Ne pas meubler.
