# Dev Notes Writer

Un skill Claude Code qui rédige, **en fin de tâche**, une note de passation propre destinée au relecteur (humain ou IA).
Il met au propre un document structuré, pour que le relecteur comprenne vite **quoi**, **pourquoi**, et **où regarder de près**.
Ajoute automatiquement, lorsque c'est pertinant, des schémas explicatifs ou des diagrammes de workflow.

## Configuration et personnalisation

### Assurer la rédaction d'une note avant un commit
Le hook "check-dev-notes-before-commit" permet de s'assurer que la note a bien été générée avant de commit. 
A configurer selon ton harness. Pour Claude Code, ajoute au settings.json : 
    {
        "matcher": "Bash",
        "hooks": [
            { "type": "command", "command": "./.claude/hooks/check-dev-notes-before-commit.sh" }
        ]
    }

### Personnaliser la structure de notes

Modifier le template : agents/dev-notes-writer/templates/dev-notes.md

## Notes produites

Un dossier daté `docs/dev-notes/AAAA-MM-JJ_HHMM_<nom-de-la-tâche>/` contenant :

- **`dev-notes.md`** — la note elle-même : contexte, décisions et compromis, difficultés rencontrées, **points d'attention pour la relecture**, fichiers modifiés.
- des **schémas explicatifs** quand une partie du code est compliquée (un diagramme vaut mieux qu'un paragraphe),
- des **diagrammes de workflow** quand un processus en plusieurs étapes a été ajouté ou modifié.

Les schémas ne sont générés que lorsqu'ils apportent vraiment quelque chose, pas pour décorer.

## Deux principes importants

- **Honnêteté avant tout** — la note remonte de vraies préoccupations, pas des phrases rassurantes. Elle explique les compromis, elle ne se contente pas de reformuler les décisions.
- **Pas d'invention** — le skill ne fabrique jamais de justification « plausible » après coup. Il documente ce qui a réellement été fait et décidé.

## Astuce pour de meilleures notes

La qualité est bien meilleure si les décisions ont été **notées au fil de l'eau** pendant le développement, plutôt que reconstruites de mémoire à la fin. 
Pense à demander à Claude de noter ses choix importants pendant qu'il code. Ou mieux, demande-lui directement dans CLAUDE.md

## Détail technique

Ce skill est implémenté sous forme d'**agent** (et non d'un simple skill) pour trois raisons : il tourne sur un modèle plus léger (économie et rapidité), il travaille dans un contexte isolé qui ne pollue pas ta session de code, et il garde une mémoire des conventions du projet d'une fois sur l'autre. Les détails d'installation et de personnalisation sont dans `agents/dev-notes-writer/README.md`.
