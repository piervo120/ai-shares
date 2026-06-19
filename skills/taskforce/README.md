# Task Force

Un skill Claude Code qui monte une **équipe d'experts virtuels** pour réfléchir à un problème compliqué sous plusieurs angles à la fois, puis en tire un plan d'action clair.
Purement expérimental. Résultats intéressants. 
Attention, skill très gourmand en tokens.

Explications générées par IA :

## L'idée en une phrase

Au lieu de demander une seule réponse à Claude, tu fais travailler en parallèle plusieurs « spécialistes » (technique, produit, business, organisation…), tu les fais se « réunir » pour confronter leurs points de vue, et tu obtiens à la fin un plan consolidé.

## Quand l'utiliser

Quand un problème est trop large ou trop transverse pour un seul angle de réflexion. Par exemple :

- « Comment lancer ce nouveau produit ? » (technique + produit + business à la fois)
- « Faut-il refondre cette application ? »
- « Monte-moi une équipe pour réfléchir à ce projet »

Le skill se déclenche quand tu demandes explicitement une « task force », « réunir des experts », « un plan à plusieurs angles », etc. Il peut aussi se proposer de lui-même si ton problème est manifestement multi-facettes.

Pour un problème simple ou à une seule dimension, ce n'est pas la peine : une réponse directe suffit.

## Comment ça se passe

1. **Cadrage** — Claude reformule ton problème, propose les angles à couvrir (et donc les experts à mobiliser), et te demande de valider. Si c'est flou, il te pose des questions avant de lancer.
2. **Travail en parallèle** — Chaque expert prépare sa note de sa propre perspective, en même temps que les autres.
3. **Réunion** — Claude joue le chef de projet : il confronte les propositions, tranche ce qui est évident, et te soumet les **décisions importantes** avec des options et une recommandation.
4. **Itérations si besoin** — De nouvelles réunions peuvent être tenues pour approfondir un point (4 réunions maximum par défaut).
5. **Plan final** — Tu obtiens un `plan.md` prêt à l'emploi, plus les notes des experts et les comptes-rendus de réunion.

## Ce que tu obtiens

Un dossier `docs/taskforce/` contenant :

- les **notes de chaque expert**,
- les **comptes-rendus de réunion** (ce qui a été décidé et pourquoi),
- un **`plan.md`** final : contexte, objectifs, décisions, étapes à suivre, risques.

Le `plan.md` est compatible avec le skill natif `/plan`.

## Ce qu'il faut savoir

- Claude ne t'interrompt que pour les **vrais arbitrages** (choix qui engagent le projet, désaccords forts entre experts). Il ne te dérange pas pour les détails.
- Les notes des experts peuvent être longues, mais elles restent dans des fichiers : seuls les comptes-rendus et le plan sont volontairement courts et denses.
