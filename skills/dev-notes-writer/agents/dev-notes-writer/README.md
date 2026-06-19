# Agent: `dev-notes-writer`

Agent Claude Code qui génère une documentation structurée en fin de tâche de coding, destinée à la personne en charge du code review.

## Ce qu'il produit

Un répertoire daté `docs/dev-notes/YYYY-MM-DD_HHMM_<feature-slug>/` contenant :

- `dev-notes.md` — note structurée (contexte, décisions, difficultés, points review, fichiers modifiés),
- des **graphiques explicatifs** pour les codes complexes (en suivant le guide bundled `prompts/explainer-graphic.md`),
- des **workflows** pour les processus multi-étapes (en suivant le guide bundled `prompts/workflow-visualizer.md`).

## Pourquoi un agent (et pas un skill) ?

Trois bénéfices par rapport à un skill équivalent :

1. **Modèle imposé** : l'agent tourne en `sonnet` (rédaction structurée), même si la session principale utilise Opus. Économie de tokens et latence réduite.
2. **Contexte isolé** : la rédaction des notes ne pollue pas le contexte de la session de coding principale.
3. **Mémoire persistante** : l'agent accumule des connaissances sur les conventions du projet, les zones sensibles, et les préférences du reviewer (`memory: project`).

## Installation

### 1. Placer l'agent

Copie le répertoire `dev-notes-writer/` dans `.claude/agents/` à la racine de ton projet (versionné dans Git) ou dans `~/.claude/agents/` pour un usage personnel multi-projets.

Structure attendue :

```
.claude/agents/
└── dev-notes-writer/
    ├── dev-notes-writer.agent.md
    ├── README.md
    ├── prompts/
    │   ├── explainer-graphic.md
    │   └── workflow-visualizer.md
    └── templates/
        └── dev-notes.md
```

### 2. Ajouter la directive dans `CLAUDE.md`

```markdown
## Documentation de fin de tâche

Pendant le développement, note au fil de l'eau les décisions de conception significatives, les alternatives écartées, et les difficultés rencontrées. À la fin de chaque tâche de coding non triviale, délègue à l'agent `dev-notes-writer` la génération de la documentation de review.
```

Cette ligne sert deux objectifs :

- **rappeler à Claude de prendre des notes pendant** le coding (l'agent n'est invoqué qu'en fin de tâche, il ne peut pas reconstruire fidèlement ce qui n'a pas été noté),
- **déclencher l'agent** au bon moment.

### 3. Vérifier que l'agent est détecté

```bash
claude agents | cat
```

L'agent `dev-notes-writer` doit apparaître dans la liste. Si non, vérifie que le frontmatter du fichier `.md` est correct et que la session Claude Code a été relancée (les agents sont chargés au démarrage de session).

## Utilisation

### Déclenchement automatique

À la fin d'une tâche de coding non triviale, Claude délègue automatiquement à cet agent grâce à sa description.

### Déclenchement explicite

En langage naturel :

```
Utilise dev-notes-writer pour préparer la doc de review
```

### Résultat attendu

```
docs/dev-notes/2026-05-14_1430_add-oauth-login/
├── dev-notes.md
├── auth-flow.md            (Mermaid, si pertinent)
└── token-refresh-state.md  (Mermaid, si pertinent)
```

## Personnalisation

### Modifier le template

Édite `templates/dev-notes.md`. La structure y est isolée pour pouvoir évoluer sans toucher au fichier de l'agent.

### Adapter le périmètre de déclenchement

Si tu veux que l'agent se déclenche même pour les petits changements, retire la mention « non triviale » dans `CLAUDE.md` et la section correspondante du fichier de l'agent.

## Limites connues

- **Sous-répertoires sous `.claude/agents/`** : la doc officielle ne montre que des exemples à plat. Cette structure en sous-répertoire fonctionne (l'agent est invoqué et lit ses prompts/templates bundled), mais reste non documentée — à surveiller en cas de changement de version de Claude Code.
- **Notes prises a posteriori** : si Claude n'a pas noté ses décisions au fil de l'eau, l'agent reconstruit de mémoire. L'agent est instruit d'être explicite dans ce cas, mais la qualité reste meilleure avec des notes progressives — d'où la ligne dans `CLAUDE.md`.
