# Dual Review

Un skill Claude Code qui fait **relire le code par deux regards différents en même temps**, puis livre une synthèse des deux.

## L'idée en une phrase

Quand on relit son propre travail, on est influencé par tout ce qu'on sait déjà du contexte. Ce skill ajoute donc un second relecteur **« à l'aveugle »**, qui découvre le code sans rien savoir de la discussion. Cette méthode permet d'augmenter significativement et simplement l'identification de bugs.

## Deux relectures en parallèle

1. **Relecture à l'aveugle** — un agent séparé qui ne connaît **rien** du contexte de la session. Il voit le code « frais », sans les justifications qui ont été échangées pendant le développement. Utile pour repérer ce qui n'est pas évident quand on n'a pas suivi.
2. **Relecture contextuelle** — la relecture normale, qui connaît **tout** l'historique de la tâche, les compromis acceptés et pourquoi.

Les deux agents tournent en parallèle. La synthèse est générée dès que les deux agents ont terminé.

## Rapport de review

- **Résumé de chaque relecture** (l'aveugle, puis la contextuelle),
- **Convergence** — les problèmes signalés par les *deux* (priorité haute, ce sont les plus fiables),
- **Divergence** — ce qu'une seule a vu :
  - vu seulement à l'aveugle = un point que le contexte « masquait »,
  - vu seulement en contextuel = souvent un compromis acceptable vu les contraintes,
- **Recommandations finales** — une liste d'actions priorisées.

