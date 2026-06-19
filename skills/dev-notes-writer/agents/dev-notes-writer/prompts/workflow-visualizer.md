# Guide : workflow

Génère un diagramme de workflow pour clarifier un processus multi-étapes, une séquence d'interactions, une machine à états, ou un cycle de vie d'objet.

## Quand générer un workflow

- Un processus avec plus de 3 étapes séquentielles ou conditionnelles.
- Une machine à états avec transitions explicites.
- Une séquence d'interactions entre composants (client → serveur → DB, par ex.).
- Un nouveau flux d'erreur ou de récupération à documenter.

**Ne pas générer** pour : une suite linéaire de 2-3 appels, un simple `if/else`, une boucle classique sur une collection.

## Choix du format

| Type de workflow | Format recommandé |
|---|---|
| Séquence d'étapes avec branches | Mermaid (`flowchart TD`) |
| Machine à états | Mermaid (`stateDiagram-v2`) |
| Interactions entre acteurs | Mermaid (`sequenceDiagram`) |
| Cycle de vie complexe | Mermaid (`stateDiagram-v2`) |

Toujours préférer Mermaid pour les workflows : la syntaxe est faite pour ça et le rendu en review est natif sur la plupart des plateformes.

## Format Mermaid : exemples

### Flowchart

````mermaid
flowchart TD
    A[Requête entrante] --> B{Token valide ?}
    B -->|Oui| C[Traiter la requête]
    B -->|Non| D[Refresh token]
    D --> E{Refresh OK ?}
    E -->|Oui| C
    E -->|Non| F[401 Unauthorized]
    C --> G[Réponse 200]
````

### Machine à états

````mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: submit()
    Submitted --> Approved: approve()
    Submitted --> Rejected: reject()
    Rejected --> Draft: edit()
    Approved --> [*]
````

### Séquence

````mermaid
sequenceDiagram
    Client->>API: POST /auth/login
    API->>DB: SELECT user
    DB-->>API: user data
    API->>API: verify password
    API-->>Client: 200 + JWT
````

## Conventions de nommage

Sauvegarde dans le répertoire dev-notes avec un nom explicite :

- `auth-flow.md`
- `order-state-machine.md`
- `payment-sequence.md`

Format du fichier : Markdown avec le bloc Mermaid à l'intérieur.

````markdown
# <Titre du workflow>

<Phrase d'intro contextuelle, 1-2 lignes.>

​```mermaid
flowchart TD
    ...
​```

<Notes complémentaires si besoin : conditions d'entrée, cas d'erreur non représentés, etc.>
````

## Référencement depuis dev-notes.md

Dans la section « Visuels » de `dev-notes.md`, ajoute :

````markdown
- [Flux d'authentification OAuth](./auth-flow.md)
- [Cycle de vie d'une commande](./order-state-machine.md)
````

## Qualité avant de livrer

- [ ] Le workflow représente la **logique réelle** du code, pas une version idéalisée.
- [ ] Les conditions de branchement sont explicites (labels sur les arêtes).
- [ ] Les cas d'erreur importants sont représentés.
- [ ] Pas plus de ~12 nœuds — sinon découpe en sous-workflows.
- [ ] Le fichier est référencé depuis `dev-notes.md`.
