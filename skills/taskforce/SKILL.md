---
name: taskforce
description: Mobilise une task force d'agents spécialisés (architecte, fonctionnel, stratège, etc.) qui investiguent en parallèle puis se réunissent pour produire un plan d'action consolidé. Utilise ce skill dès que l'utilisateur veut "monter une équipe", "réunir des experts", "lancer une task force", "préparer un plan à plusieurs angles", "orchestrer une réflexion collective", ou demande un plan qui nécessite plusieurs expertises distinctes (technique + produit + business, par exemple). Déclenche-toi aussi quand un problème est manifestement multi-facettes même si l'utilisateur ne demande pas explicitement une task force — propose alors de l'utiliser. Produit des comptes-rendus de réunion, des livrables d'agents, et un plan.md final compatible avec le skill /plan natif.
---

# Task Force

Orchestre une équipe d'agents spécialisés qui travaillent en parallèle, se réunissent, itèrent, et produisent un plan d'action structuré.

## Principe

Pour un problème non-trivial, un seul angle de réflexion suffit rarement. Ce skill simule un comité d'experts :

1. Le problème est découpé en angles (structurel, architecture, fonctionnel, stratégique, et autres selon le contexte)
2. Un agent spécialisé est assigné à chaque angle
3. Les agents préparent leur intervention **en parallèle** (vrais sub-agents via Task tool)
4. Une réunion est tenue : ordre du jour, échanges, décisions, plan d'action
5. Si nécessaire, de nouvelles réunions sont organisées (recherche complémentaire, arbitrage, etc.)
6. À la fin, un `plan.md` final est produit, exploitable par le skill `/plan` natif

Le **chef de projet** est l'agent qui orchestre. Le **secrétaire** prend des notes structurées. Ces deux rôles sont obligatoires et systématiques.

## Workflow

### Étape 1 — Cadrage avec l'utilisateur

Avant tout, reformule la problématique en une phrase, puis identifie les angles pertinents. Les angles par défaut sont :

- **Structurel** — organisation, équipe, processus, gouvernance
- **Architecture** — choix techniques, intégrations, scalabilité, dette
- **Fonctionnel** — usages, parcours utilisateur, périmètre, exigences
- **Stratégique** — alignement business, ROI, risques, priorisation

Tu peux **ajouter ou retirer** des angles selon la problématique (ex. ajouter "data", "sécurité", "légal", "design"). Tu peux aussi **fusionner** deux angles s'ils se recoupent fortement sur ce projet précis.

Propose à l'utilisateur la liste d'angles retenus avec, pour chacun, le **profil d'agent** correspondant (3-5 mots décrivant son expertise). Demande validation avant de lancer.

Si la problématique est floue, **demande des clarifications** maintenant — pas plus tard. Concentre-toi sur : périmètre, contraintes connues, objectif mesurable, contexte technique/business.

### Étape 2 — Mise en place de l'arborescence

Crée immédiatement la structure de fichiers :

```
docs/taskforce/
├── meetings/           # un fichier .md par réunion
├── agents/             # livrables par agent (briefings, recherches, propositions)
└── plan.md             # plan final consolidé (généré à la fin)
```

Vérifie d'abord si `docs/` existe déjà — si oui, ne pas écraser, juste ajouter les sous-dossiers manquants.

### Étape 3 — Briefing initial des agents (en parallèle)

Pour chaque angle identifié, lance un sub-agent via le Task tool. **Tous les Task calls partent dans le même message** pour exécution réellement parallèle.

Chaque agent reçoit :
- Sa fiche de rôle (voir `references/agent-roles.md` pour le template de prompt)
- Le contexte complet de la problématique
- La consigne de produire un **briefing note** dans `docs/agents/<nom-agent>-briefing-r1.md`

Le briefing note suit le template `assets/briefing-template.md` :
- Compréhension du problème depuis l'angle de l'agent
- 2 à 4 propositions concrètes (pas juste des principes)
- Risques et points de vigilance
- Questions ouvertes à débattre en réunion
- Dépendances vis-à-vis des autres angles

Pendant que les agents travaillent, **prépare en amont l'ordre du jour** de la première réunion (5-8 points à arbitrer, basés sur ce que tu anticipes des angles).

### Étape 4 — Tenue de la réunion

Quand tous les briefings sont rentrés, le **chef de projet** (toi, dans ce rôle) :

1. Lit tous les briefings
2. Confronte les propositions : où elles convergent, où elles s'opposent
3. Identifie les **décisions clés à prendre** et celles qui sont évidentes
4. Pour les décisions évidentes : tranche
5. Pour les décisions clés non évidentes : **présente la synthèse à l'utilisateur** avec options et recommandation, et demande validation

Pendant la réunion, le **secrétaire** (autre rôle que tu endosses, en interne) tient le compte-rendu dans `docs/meetings/rN-<slug>.md` selon le template `assets/meeting-template.md` :

- Ordre du jour
- Participants (liste des agents + rôles)
- Points saillants par sujet
- Décisions actées (avec justification courte)
- Plan d'action (tâche, owner, échéance estimée)
- Questions ouvertes / sujets reportés

`N` est le numéro de réunion (`r1`, `r2`, …). Le slug décrit le thème principal (`r1-cadrage`, `r2-arbitrage-archi`).

### Étape 5 — Décision d'itérer ou de conclure

Après chaque réunion, le chef de projet décide :

**Itérer (nouvelle réunion)** si l'une de ces conditions est remplie :
- Un agent doit approfondir un sujet (lance-le en sub-agent avec une mission précise)
- Une décision majeure reste bloquée et nécessite plus de matière
- L'utilisateur a demandé une révision sur un point

**Conclure** si :
- Toutes les décisions clés sont actées
- Le plan d'action est cohérent et exécutable
- Aucun agent n'a de point bloquant restant
- **Garde-fou** : maximum 4 réunions par défaut. Au-delà, prévenir l'utilisateur et lui demander si on continue ou si on finalise avec ce qu'on a.

Si nouvelle réunion : retour à l'étape 3 avec une mission ciblée pour les agents concernés (pas tous systématiquement — relance uniquement ceux qui ont du travail à refaire).

### Étape 6 — Production du `plan.md` final

Une fois conclu, génère `docs/plan.md` au format compatible avec le skill `/plan` natif. Voir `assets/plan-template.md`. Structure :

- **Contexte** (2-3 phrases)
- **Objectifs** (mesurables si possible)
- **Décisions structurantes** (issues des réunions, avec lien vers le CR qui les a actées)
- **Plan d'action** : liste ordonnée d'étapes avec owner, dépendances, critère de complétion
- **Risques et mitigations**
- **Annexes** : liens vers les briefings d'agents et les CR de réunion

À la fin, présente à l'utilisateur un récapitulatif court (5-10 lignes) et liste les fichiers produits.

## Règles de fonctionnement

### Parallélisme réel

Quand tu lances plusieurs agents (étape 3 ou étape 5 si plusieurs en relance), **tous les Task calls partent dans le même message**. C'est ce qui rend les agents réellement simultanés. Lancer les agents un par un dans des messages séparés est une erreur — c'est du séquentiel déguisé.

### Spécialisation des agents

Le prompt de chaque sub-agent doit être **incisif** : pas "tu es un expert", mais "tu es l'architecte technique chargé de l'angle X, tu ne dois pas déborder sur Y qui est traité par un autre agent". Voir `references/agent-roles.md` pour les patterns.

Si tu détectes qu'un agent déborde sur le périmètre d'un autre dans son briefing, signale-le dans le CR sous "questions ouvertes" — c'est souvent un signe que les frontières sont mal posées et qu'il faut clarifier le découpage.

### Quand interrompre l'utilisateur

L'utilisateur a explicitement choisi un mode "synthèse + validation des décisions clés". Donc :

- **Ne pas l'interrompre** pour des détails opérationnels, des choix de nommage, des décisions techniques bien tranchées par les agents
- **L'interrompre** pour : arbitrages stratégiques, divergences fortes entre agents, choix qui engagent le projet sur plusieurs mois, ambiguïté du périmètre détectée tardivement

Quand tu l'interromps, présente toujours : la question, les options avec leurs trade-offs, la recommandation du chef de projet, et ce qui se passe selon chaque choix.

### Économie de tokens

Les briefings d'agents peuvent être longs et c'est OK — ils sont dans des fichiers, pas en contexte permanent. Mais le **CR de réunion doit être dense** : ce qui s'est dit, pas un copier-coller des briefings. Pareil pour `plan.md` : concis, actionnable, pas un résumé exhaustif.

### Évolutivité

Si en cours de route un nouvel angle apparaît (ex. on se rend compte qu'il faut un volet "sécurité"), **ne pas tout recommencer**. Lance un agent supplémentaire ciblé sur ce nouvel angle, intègre son briefing à la réunion suivante.

## Ressources

- `references/agent-roles.md` — Patterns de prompts pour chaque type d'agent (architecte, fonctionnel, stratège, chef de projet, secrétaire, et profils additionnels)
- `assets/briefing-template.md` — Template du briefing note que chaque agent produit avant réunion
- `assets/meeting-template.md` — Template du compte-rendu de réunion
- `assets/plan-template.md` — Template du `plan.md` final
