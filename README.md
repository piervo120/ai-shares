# ai-shares

Partage de **skills, agents, prompts et hooks expérimentaux** pour Claude Code (ou tout autre harness compatible).

Ce dépôt rassemble des briques que j'utilise et que je teste pour outiller un agent de code. C'est **expérimental** : les résultats sont intéressants mais la personnalisation pour votre workflow de dev et d'équipe est clé. À forker, adapter et améliorer librement.

## Contenu

| Élément | Type | En une phrase |
|---|---|---|
| [`taskforce`](skills/taskforce/) | Skill | Monte une équipe d'experts virtuels qui réfléchissent en parallèle, se réunissent, et produisent un plan d'action consolidé. |
| [`prism-review`](skills/prism-review/) | Skill | Fait relire le code par trois regards en parallèle (à l'aveugle, contextuel, et Codex nourri de la seule intention du plan), puis livre une synthèse qui explique pourquoi chaque voix a vu ce qu'elle a vu. |
| [`dual-review`](skills/dual-review/) | Skill | Variante légère de `prism-review` : deux regards en parallèle (un « à l'aveugle » sans contexte + un contextuel), puis une synthèse. |
| [`dev-notes-writer`](skills/dev-notes-writer/) | Agent | Rédige en fin de tâche une note de passation structurée pour le relecteur, schémas à l'appui. |
| [`hooks/`](hooks/) | Hooks | Garde-fous côté agent : bloque les commandes destructives et protège les fichiers sensibles/générés. |

Chaque skill a son propre `README.md` détaillé dans son dossier.

## Installation

> Certains skills embarquent leur sous-arborescence complète (ex. `dual-review/skills/dual-review/`, `dev-notes-writer/agents/dev-notes-writer/`) pour pouvoir être copiés tels quels vers leur cible. Le chemin interne est la vraie destination ; le dossier `skills/<nom>/` qui l'entoure n'est qu'un emballage.

### Hooks

Les hooks sont des garde-fous `PreToolUse` (autoriser / bloquer une action de l'agent). Un exemple de configuration est fourni dans [`hooks/settings.json`](hooks/settings.json) — à adapter à ton harness. Pour Claude Code, copie les scripts dans `.claude/hooks/` et reporte les entrées correspondantes dans ton `settings.json`.

- `block-dangerous.sh` — bloque les commandes destructives (`git push --force`, `reset --hard`, `rm -rf`…).
- `protect-files.sh` — bloque l'édition de fichiers générés ou sensibles (`.env`, lock files, fichiers générés…).
- `check-dev-notes-before-commit.sh` / `.ps1` — empêche un commit tant que la dev-note du jour n'a pas été produite (livré avec `dev-notes-writer`).

Ce sont des **garde-fous côté agent** (défense en profondeur), pas une frontière de sécurité : ils n'affectent ni la CI ni un accès direct au système de fichiers.

## Licence

Libre d'usage, fork et amélioration.