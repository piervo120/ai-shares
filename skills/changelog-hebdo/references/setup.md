# Setup — première utilisation dans un projet

Objectif : produire `docs/changelog/changelog.config.md` (à partir de `config-template.md`), validé par l'utilisateur. Ne pas générer de changelog avant que la config existe.

## 1. Explorer le dépôt (auto)

Chercher, sans rien demander encore :

- **Conventions de commit** : `git log -30 --pretty=format:'%s'` — conventional commits ? langue ? types/scopes utilisés ?
- **Docs de contexte des changements** : dev-notes, ADR, PR descriptions, dossiers `docs/` datés — où vit le « pourquoi » des changements ?
- **Registre d'incidents / fiabilité** : fichiers de suivi de problèmes, post-mortems, dashboards.
- **Sources de preuves chiffrées** : rapports générés (CSV, JSON), métriques, analytics — relever les **noms de fichiers et de champs exacts** ; noter si versionnés (toujours disponibles) ou générés au runtime (parfois absents).
- **Contexte produit** : README, docs produit — quelle est la proposition de valeur ? existe-t-il une métrique de valeur centrale (formule) ? des idées reçues à ne PAS signaler comme anomalies ?
- **Changelog existant** : réutiliser l'emplacement et ne pas casser le format s'il y en a un.

## 2. Questions à l'utilisateur (seulement le non-déductible)

Poser uniquement ce que l'exploration n'a pas tranché, typiquement :

1. **Audience** : qui lit ? niveau technique ? langue ?
2. **Métrique de valeur** : sur quel axe ancrer les bénéfices (revenu, coût, risque, rétention…) si aucune formule n'a été trouvée ?
3. **Emplacement de sortie** si un autre dossier que `docs/changelog/` est souhaité.

## 3. Rédiger et valider

1. Instancier `config-template.md` avec les découvertes + réponses. Chaque source doit citer des **chemins et champs réels vérifiés** (pas de placeholders restants).
2. Présenter le brouillon à l'utilisateur pour validation.
3. Écrire `docs/changelog/changelog.config.md`, puis reprendre le flux normal du skill.
