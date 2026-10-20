# ai-shares

Partage de **skills, agents, prompts et hooks expérimentaux** pour Claude Code (ou tout autre harness compatible).

Ce dépôt rassemble des briques que j'utilise et que je teste pour outiller un agent de code. C'est **expérimental** : les résultats sont intéressants mais la personnalisation pour votre workflow de dev et d'équipe est clé. À forker, adapter et améliorer librement.

## Contenu

| Élément | Type | En une phrase |
|---|---|---|
| [`taskforce`](skills/taskforce/) | Skill | Monte une équipe d'experts virtuels qui réfléchissent en parallèle, se réunissent, et produisent un plan d'action consolidé. |
| [`prism-review`](skills/prism-review/) | Skill | Fait relire le code par trois regards en parallèle (à l'aveugle, contextuel, et Codex nourri de la seule intention du plan), puis livre une synthèse qui explique pourquoi chaque voix a vu ce qu'elle a vu. |
| [`dual-review`](skills/dual-review/) | Skill | Variante légère de `prism-review` : deux regards en parallèle (un « à l'aveugle » sans contexte + un contextuel), puis une synthèse. |
| [`open-plan-review`](skills/open-plan-review/) | Skill | Fait relire un plan d'implémentation par trois relecteurs indépendants et à l'aveugle (Claude Opus, Claude Sonnet, Codex), puis par un agent de synthèse adversarial qui apparie les convergences, challenge les constats isolés et propose des amendements. |
| [`changelog-hebdo`](skills/changelog-hebdo/) | Skill | Produit un changelog hebdomadaire pour des décideurs non techniques : commits et docs traduits en valeur métier, preuves chiffrées traçables, registre de valeur suivi dans le temps. |
| [`dev-notes-writer`](skills/dev-notes-writer/) | Agent | Rédige en fin de tâche une note de passation structurée pour le relecteur, schémas à l'appui. |
| [`hooks/`](hooks/) | Hooks | Garde-fous côté agent : bloque les commandes destructives et protège les fichiers sensibles/générés. |

`taskforce`, `prism-review`, `dual-review` et `dev-notes-writer` ont leur propre `README.md` détaillé dans leur dossier ; `open-plan-review` et `changelog-hebdo` se décrivent dans leur `SKILL.md`.

`open-plan-review` s'appuie sur deux agents, `plan-reviewer` et `plan-synthesizer`, attendus dans `.claude/agents/` et non fournis dans ce dépôt. `prism-review` suppose Python 3 ; Codex CLI y est facultatif.

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