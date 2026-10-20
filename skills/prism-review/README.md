# Prism Review

Un skill Claude Code qui fait relire un développement par **trois regards différents en même temps**, puis livre une synthèse qui dit pourquoi chacun a vu ce qu'il a vu.

Successeur de [`dual-review`](../dual-review/), qui reste disponible comme variante légère à deux voix.

## L'idée en une phrase

Un même diff, décomposé comme par un prisme : une lecture qui ignore tout du contexte, une lecture qui le connaît, et une lecture qui ne connaît que ce que le chantier devait garantir. Les trois ne se recouvrent pas par construction — et c'est leur écart qui révèle les défauts.

## Trois relectures en parallèle

1. **À l'aveugle** — un sous-agent (`prism-blind-reviewer`) qui ne sait **rien** de la session. Il voit le code « frais », sans les justifications échangées pendant le développement.
2. **Contextuelle** — la session elle-même, qui connaît l'historique, les compromis acceptés et pourquoi.
3. **Par l'intention (Codex)** — une revue Codex à qui l'on ne transmet que le *pourquoi* et les *garanties* du plan, jamais l'implémentation. C'est elle qui juge le code contre ce qu'il était censé garantir plutôt que contre lui-même, et qui trouve les chemins d'exécution que seule l'intention rend visibles.

## Rapport de revue

- **Résumé de chaque relecture**, avec marquage `[P1]` / `[P2]` ;
- **Convergence** — ce que plusieurs voix pointent (priorité haute) ;
- **Divergence** — ce qu'une seule a vu, avec **pourquoi elle seule pouvait le voir** : le contexte masquait le problème (aveugle), compromis acceptable (contextuelle), chemin visible par l'intention seule (Codex) ;
- **Recommandations** priorisées.

## Contenu

| Fichier | Installe vers | Rôle |
|---|---|---|
| `skills/prism-review/SKILL.md` | `.claude/skills/prism-review/` | L'orchestration en cinq étapes. |
| `skills/prism-review/references/review-rubric.md` | idem | Grille commune aux trois voix : axes, marquage, format. Remplace toute dépendance à un skill `code-reviewer`. |
| `skills/prism-review/scripts/build-codex-prompt.py` | idem | Assemble le prompt Codex (grille + brief + fichiers numérotés), sous budget, en UTF-8 forcé. |
| `skills/prism-review/scripts/test-build-codex-prompt.py` | idem | Banc d'essai du script. |
| `agents/prism-blind-reviewer/prism-blind-reviewer.md` | `.claude/agents/prism-blind-reviewer/` | Le relecteur à l'aveugle (modèle `sonnet`, lecture seule). |

## Prérequis

- **Python 3** pour le script de prompt.
- **Codex CLI** — *facultatif*. Absent ou en échec, le skill le signale dans le rapport et poursuit en revue duale (aveugle + contextuelle).
- Un dépôt git, pour délimiter le lot de fichiers à relire.

Le skill ne présuppose aucun langage ni outil de build : il lit les commandes de vérification que le projet déclare (`CLAUDE.md`, `README`, `Makefile`, `package.json`…) et les lance une fois avant les revues.

## Installation

Copier `agents/prism-blind-reviewer/` vers `.claude/agents/` et `skills/prism-review/` vers `.claude/skills/` (projet, ou `~/.claude/` pour tous les projets). Les agents ne se chargent qu'au démarrage d'une session : rouvrir la session après installation.

---

🛠️ Crafted by Pierre Vaussanvin — Free to use, fork & improve.
