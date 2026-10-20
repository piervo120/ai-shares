---
name: prism-review
description: Revue de code en trois regards parallèles après un développement — un sous-agent à l'aveugle (sans contexte), une revue contextuelle (contexte complet de la session) et une revue Codex nourrie de la seule intention du plan — puis un rapport de synthèse qui dit pourquoi chaque voix a vu ce qu'elle a vu. À utiliser quand on dit « relis mon code », « revue avant commit », « fais relire ce développement », « revue à l'aveugle », « trois regards », « double revue », ou en fin de développement avant de committer.
---

Lancer trois revues en parallèle et rendre un rapport de synthèse.

Les trois voix ne se recouvrent pas par construction : l'aveugle juge le code sans savoir
pourquoi il est ainsi, la contextuelle le juge en connaissant les contraintes, et Codex le juge
contre ce que le chantier était censé garantir. C'est cette troisième lecture qui trouve les
chemins d'exécution impossibles — ceux qu'on ne voit qu'en sachant ce que le dispositif promet.

Le skill ne sait rien du projet courant. Il découvre la racine, les commandes de vérification et
les fichiers du lot au moment de l'exécution.

## Étape 0 — Établir les faits, une seule fois

- **La racine** : `git rev-parse --show-toplevel`, sinon le répertoire courant.
- **Le dossier du skill** (`SKILL_DIR`) : `<racine>/.claude/skills/prism-review` s'il existe, sinon
  `~/.claude/skills/prism-review`. Les chemins `references/…` et `scripts/…` ci-dessous en sont
  relatifs.
- `SC` = répertoire scratchpad de la session.
- **Les vérifications du projet** : build, tests, linters, tels que le dépôt les déclare — section
  « build/test » de `CLAUDE.md` ou `AGENTS.md`, `README`, `Makefile`, `package.json`, CI. Rien de
  découvrable : le dire dans le brief et dans le rapport plutôt que d'inventer une commande.

Lancer ces vérifications dans cette session, une fois, avant tout lancement de relecteur.
Aucun relecteur ne les relance : deux builds concurrents se disputent les mêmes artefacts et
produisent des échecs fantômes, et des tests déterministes ne livrent rien au second passage.

Transmettre la **sortie brute** des commandes à chaque relecteur — la ligne de commande et son
résultat, pas ta lecture du résultat. Un résultat de test est un fait vérifiable et ne biaise pas
la revue à l'aveugle ; une conclusion sur ce résultat, si.

Build ou tests en échec : s'arrêter, corriger, reprendre à l'étape 0.

**L'arbre doit rester stable pendant les revues.** Ne modifier aucun fichier du lot entre le
lancement et la réception des trois rapports — un relecteur qui lit un fichier en cours d'édition
rend des constats sur du code qui n'existe plus.

**Le lot** (liste des fichiers à relire), dans `$SC/files.txt`, un chemin par ligne, relatif à la
racine :

```bash
cd "$(git rev-parse --show-toplevel)"   # git ls-files rend des chemins relatifs au répertoire courant, git diff à la racine
{ git -c core.quotePath=false diff --name-only HEAD; git -c core.quotePath=false ls-files --others --exclude-standard; } | sort -u > "$SC/files.txt"
```

`core.quotePath=false` évite que git cite et échappe les noms non ASCII (`résumé.md`), que le script
ne retrouverait pas sur le disque. Hors dépôt git, ces commandes ne rendent rien : dresser
`files.txt` à la main.

Le tri est alphabétique : réordonner à la main, code neuf d'abord, contrats (docs, README,
`SKILL.md`) ensuite, ce qui a déjà été relu en dernier — le budget de l'étape 2 écarte les
derniers fichiers.

Arbre propre (travail déjà committé) : `git -c core.quotePath=false diff --name-only $(git merge-base HEAD <branche-de-base>)`.
Retirer de la liste ce qui n'appartient pas au chantier — l'arbre contient parfois le travail
d'une autre session — et ce qui est généré.

## Étape 1 — Construire le brief d'intention pour Codex

Le point sensible de tout le dispositif. Passer le plan **entier** à Codex annule le bénéfice :
avec les sections d'implémentation sous les yeux, il compare le code au code et retombe dans
l'angle des deux autres revues. Et cet échec est **silencieux** — on croit avoir fait la revue.

**Trouver le plan** : le plus récent de `~/.claude/plans/*.md` qui cite le projet courant. À
défaut de correspondance, prendre le plus récent en signalant dans le brief qu'il peut venir d'un
autre projet. Aucun plan → reconstruire l'intention (plus bas).

**Le critère de tri**, à poser comme une question à chaque section :

| Garder — ce qui répond à | Retirer — ce qui répond à |
|---|---|
| pourquoi ce chantier existe | quels fichiers modifier |
| quel défaut il ferme, et pourquoi il est grave | quel code écrire, quelle signature |
| ce que le résultat doit garantir | dans quel ordre procéder |
| les invariants, contrats, garde-fous | quels tests ajouter, quelles commandes lancer |
| les bornes du périmètre | quelles bibliothèques réutiliser |

Trier par **contenu**, jamais par niveau de titre ni par numérotation. Les garde-fous se cachent
parfois en `###` sous une section d'implémentation : **aller les chercher et les remonter**. La
section de vérification se garde **reformulée en garanties**, sans les commandes. Tout ce qui ne
figure pas dans la colonne « Garder » (annexes d'outils, rapports de revue) est exclu.

`## Contexte` (ou `## Context`) ouvre la plupart des plans et est toujours de l'intention. Un plan
peut en revanche n'avoir aucune section d'intention distincte — le pourquoi y est noyé dans un
`## Context` mêlé de noms de méthodes. Il faut alors le **reformuler**, pas le recopier.

**Sans plan écrit** : rédiger le brief depuis la conversation — ce qu'on cherchait à faire, quel
défaut on fermait, ce que le résultat doit garantir, ce qui était hors périmètre. Le **dire dans
le brief**, pour que Codex sache que l'intention est reconstruite et non citée.

Le brief se termine par une section **Périmètre** : les bornes du chantier et, le cas échéant, les
fichiers du lot que Codex ne verra pas. C'est le seul endroit du brief où des chemins sont admis.

**Auto-contrôle avant envoi** :

- [ ] aucun chemin de fichier du lot dans le brief, hors la section « Périmètre »
- [ ] aucun bloc de code d'implémentation
- [ ] aucun nom de fonction, de classe ou de constante introduits par le lot
- [ ] chaque paragraphe conservé relève de la colonne « Garder »
- [ ] les garanties du plan sont là, **y compris celles qui étaient en `###`**

Un seul point en échec et Codex comparera le code au code : la revue ne rendra rien que les deux
autres n'auraient trouvé.

Écrire le brief dans `$SC/brief-codex.md`.

## Étape 2 — Lancer les trois en parallèle

Dans un **même message**, sans attendre entre les lancements :

1. `@prism-blind-reviewer` — sous-agent, sans contexte, en tâche de fond. Son prompt contient :
   la liste des fichiers du lot, le chemin `SKILL_DIR/references/review-rubric.md`, la sortie
   brute des vérifications de l'étape 0. **Pas** le brief, pas la conversation. Jamais
   `subagent_type: "fork"` — un fork hérite de la conversation, ce qu'exclut la revue à l'aveugle.
2. **Codex** — commande Bash en arrière-plan (`run_in_background`).
3. La revue contextuelle — dans cette session, avec tout le contexte, selon
   `SKILL_DIR/references/review-rubric.md`, pendant que les deux autres tournent.

### L'invocation Codex

Contraintes de la machine, chacune fatale si on l'oublie :

- sous Windows, le binaire n'est pas dans le `PATH` tant que la session n'a pas été rouverte,
  d'où le préfixe ;
- le sandbox lecture seule ne démarre pas sous Windows natif, donc **tout le contenu à relire est
  embarqué dans le prompt** et Codex reçoit l'ordre de n'exécuter aucune commande ;
- `argv` est plafonné à 32 Ko sous Windows, donc le prompt passe par **stdin** (`codex exec -`) ;
- la sortie standard de Python est en **cp1252** sous Windows, pas en UTF-8 : sans correctif, un
  script qui imprime la première flèche ou le premier `≥` meurt après n'avoir écrit que l'en-tête,
  et comme `codex exec` est une commande distincte, il part quand même, avec un prompt vidé de
  tout le code. Codex répond « aucun code à relire » et **on croit avoir fait la revue**. Le script
  force l'UTF-8 ; le garde-fou ci-dessous transforme l'échec silencieux restant en échec franc ;
- **le modèle est épinglé**, parce que le défaut du binaire (`~/.codex/config.toml`) peut être
  refusé par le compte du jour au lendemain : un 400 « not supported when using Codex with a
  ChatGPT account » rend un fichier vide qui ressemble à une panne de Codex.

```bash
export PATH="$HOME/AppData/Local/Programs/OpenAI/Codex/bin:$PATH"   # Windows ; ailleurs, codex est déjà dans le PATH
CODEX_MODEL="gpt-5.6-sol"   # à ajuster : voir « Codex indisponible »

python "$SKILL_DIR/scripts/build-codex-prompt.py" \
  --brief "$SC/brief-codex.md" \
  --rubric "$SKILL_DIR/references/review-rubric.md" \
  --files-from "$SC/files.txt" > "$SC/codex-prompt.txt"

# Un prompt amputé rend une revue vide qui ressemble à une revue faite : échouer franchement.
if ! grep -q "===== FICHIER" "$SC/codex-prompt.txt"; then
  echo "Prompt Codex incomplet : le code n'a pas été embarqué. Poursuivre en revue duale."; exit 1
fi
head -12 "$SC/codex-prompt.txt"

codex exec - -m "$CODEX_MODEL" -c 'model_reasoning_effort="high"' -o "$SC/review-codex.md" \
  < "$SC/codex-prompt.txt" > "$SC/codex-out.txt" 2>"$SC/codex-err.txt"
```

Le script numérote les lignes, ce qui permet à Codex de citer `fichier:ligne` exactement — sans
numéros ses constats deviennent invérifiables. `-o` capture la seule réponse finale ; la bannière
et la trace restent dans `codex-out.txt` / `codex-err.txt`.

**Borne de taille** : le prompt est plafonné à 150 Ko par défaut (`--budget-kb`). Les fichiers qui
n'y tiennent pas sont **écartés et listés dans les premières lignes du prompt** : les lire, puis
**le dire dans la section « Périmètre » du brief (puis régénérer le prompt) et dans le rapport**
— un périmètre réduit en silence se lit comme une couverture complète. Le script remplit le budget
dans l'ordre de `files.txt` : mettre en tête le code neuf et les contrats, en queue ce qui a déjà
été relu.

**Ce que Codex doit chercher** : les axes de la grille, dans son ordre de priorité —
l'implémentation trahit-elle le plan ; divergences entre le contrat écrit et le code ; invariants
sur les séquences tordues ; ce que les tests ne couvrent pas ; sécurité de base ; sur-complexité.

**Codex indisponible** — binaire absent, authentification manquante, code de retour non nul,
`review-codex.md` vide : si `codex-err.txt` porte un 400 qui nomme le modèle, sonder une fois un
autre identifiant (`echo OK | codex exec -m <id> -`) et relancer avec lui. Sinon, ou si la relance
échoue, le signaler dans le rapport avec la commande qui a échoué, et poursuivre en revue duale.
Ne jamais rien installer sans demander.

**Type d'agent introuvable** (« Agent type 'prism-blind-reviewer' not found ») : la session a été
ouverte avant l'installation de l'agent, qui ne se charge qu'au démarrage. Lancer alors
`subagent_type: "general-purpose"`, `model: "sonnet"`, avec le corps de l'agent collé en tête du
prompt.

## Étape 3 — Attendre les trois

Attendre que les trois revues soient rendues avant de poursuivre.

## Étape 4 — Rapport de synthèse

Un rapport Markdown structuré ainsi :

### 🔍 Revue à l'aveugle
[Constats du sous-agent, sans contexte]

### 🧠 Revue contextuelle
[Constats de la revue en session, avec tout le contexte]

### 🤖 Revue Codex
[Constats issus de l'intention seule, avec leur marquage [P1] / [P2]]

### ⚡ Convergence — plusieurs revues pointent la même chose
[Priorité haute]

### 🔀 Divergence — une seule revue l'a vu
Pour chaque constat, dire **pourquoi elle seule pouvait le voir** :
- aveugle seule : le contexte masquait le problème ;
- contextuelle seule : compromis acceptable au vu des contraintes ;
- Codex seul : chemin d'exécution que seule l'intention rend visible.

Cette colonne est ce qui rend le dispositif lisible : elle dit si la troisième voix a payé sur ce
lot, ou si elle a doublonné.

### ✅ Recommandations
Liste priorisée.

---

🛠️ Crafted by Pierre Vaussanvin — Free to use, fork & improve.
