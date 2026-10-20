---
name: open-plan-review
description: Fait relire un plan d'implémentation par trois relecteurs indépendants et à l'aveugle (Claude Opus, Claude Sonnet, Codex/OpenAI) dans un cadre de sortie unique, puis par un agent de synthèse adversarial qui apparie les convergences, challenge chaque constat isolé contre le plan et le dépôt, et propose des amendements. À la demande, sur n'importe quel projet, typiquement avant ExitPlanMode. Invocation : /open-plan-review [chemin-du-plan].
---

Faire relire un plan par un panel multi-LLM, synthétiser, et laisser l'utilisateur trancher.

Le plan est relu **à l'aveugle** : aucun relecteur n'a la conversation qui l'a produit. C'est
voulu — ce qui manque au plan manquera à celui qui l'exécute. Trois voix, deux familles de
modèles : deux Claude sur des modèles différents, et Codex. Un agent de synthèse distinct de la
session apparie, challenge et propose. La session, elle, n'évalue rien : elle a écrit le plan,
elle est juge et partie.

Le skill ne sait rien du projet courant. Il découvre la racine, les fichiers de conventions et
les fichiers cités par le plan au moment de l'exécution.

## Étape 0 — Localiser et figer

- **Le plan** : le chemin passé en argument. Sinon, parmi `~/.claude/plans/*.md`, ceux qui citent
  le nom du répertoire du projet courant : une ou plusieurs correspondances → le plus récent ;
  aucune → le plus récent de tous. Dans les deux cas, **nommer le plan retenu** dans le message
  d'ouverture, avec la règle qui l'a choisi.
- **La racine** : `git rev-parse --show-toplevel`, sinon le répertoire courant.
- **Les conventions** : parmi `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` à la racine, ceux qui
  existent. Aucun n'est obligatoire.
- **Le cadre** : `~/.claude/skills/open-plan-review/references/review-frame.md`, lu une fois et
  transmis verbatim aux relecteurs Claude. Le script de l'étape 1 l'embarque pour Codex.
- `SC` = répertoire scratchpad de la session.

**Ne modifier ni le plan ni l'arbre** entre le lancement et la réception des revues : un
relecteur qui lit un fichier en cours d'édition rend des constats sur ce qui n'existe plus.

## Étape 1 — Construire le prompt Codex

```bash
SC="<répertoire scratchpad de la session>"
python ~/.claude/skills/open-plan-review/scripts/build-codex-prompt.py \
  --plan "<chemin du plan>" \
  --frame ~/.claude/skills/open-plan-review/references/review-frame.md \
  > "$SC/codex-prompt.txt"

# Un prompt amputé rend une revue vide qui ressemble à une revue faite : échouer franchement.
if ! grep -q "## Verdict" "$SC/codex-prompt.txt" || ! grep -q "===== PLAN" "$SC/codex-prompt.txt"; then
  echo "Prompt Codex incomplet. Poursuivre à deux voix et le signaler."; exit 1
fi
head -12 "$SC/codex-prompt.txt"
```

Le script embarque, dans l'ordre : le cadre, le plan numéroté, les fichiers de conventions, puis
les fichiers **cités par le plan** qui existent. Le budget (150 Ko par défaut, `--budget-kb`)
plafonne le prompt entier, mais **seuls les fichiers cités peuvent être écartés** : cadre, plan et
conventions passent toujours en entier. Un chemin absolu sous la racine est ramené en relatif ;
un chemin `~/…` ou `$…` n'est pas un chemin du dépôt et n'est ni résolu ni listé ; un chemin
absolu hors de la racine est listé « hors dépôt ». Les premières lignes du prompt listent les
fichiers cités non embarqués (inexistants — souvent ceux que le plan va créer —, hors dépôt, ou
hors budget) : les lire, et transmettre cette liste à la synthèse — un périmètre réduit en silence
se lit comme une couverture complète. `--repo` force la racine.

## Étape 2 — Lancer les trois dans un même message

Sans attendre entre les lancements, en tâche de fond. **Jamais `subagent_type: "fork"`** — un
fork hérite de la conversation, ce qui est exactement ce que la relecture à l'aveugle exclut.

1. `Agent`, `subagent_type: "plan-reviewer"`, `model: "opus"`. Le prompt contient : le chemin du
   plan, la racine, la liste des fichiers de conventions trouvés (ou « aucun »), le cadre
   **verbatim**, le préfixe `CO-`, le chemin de sortie `$SC/review-opus.md`.
2. Idem avec `model: "sonnet"`, préfixe `CS-`, sortie `$SC/review-sonnet.md`.
3. Codex, commande Bash en arrière-plan :

```bash
export PATH="$HOME/AppData/Local/Programs/OpenAI/Codex/bin:$PATH"
CODEX_MODEL="gpt-5.5"   # le seul accepté par le compte ChatGPT au 2026-09-17 ; voir plus bas
codex exec - -m "$CODEX_MODEL" -c 'model_reasoning_effort="high"' -o "$SC/review-codex.md" \
  < "$SC/codex-prompt.txt" > "$SC/codex-out.txt" 2>"$SC/codex-err.txt"
```

Quatre contraintes de la machine, pas du projet : le binaire n'est pas dans le `PATH` tant que la
session Windows n'a pas été rouverte ; le sandbox lecture seule ne démarre pas sous Windows
natif, donc tout est embarqué et Codex reçoit l'ordre de n'exécuter aucune commande ; `argv` est
plafonné à 32 Ko sous Windows, donc le prompt passe par stdin ; et **le modèle est épinglé**, parce
que le défaut du binaire (`~/.codex/config.toml`) peut être refusé par le compte du jour au
lendemain — le 2026-09-17, `gpt-5.4` et tous les `gpt-5.x-codex` rendaient un 400 « not supported
when using Codex with a ChatGPT account » et seul `gpt-5.5` passait. `-o` capture la seule réponse
finale ; la bannière et la trace restent dans `codex-out.txt` / `codex-err.txt`.

**Type d'agent introuvable** (« Agent type 'plan-reviewer' not found ») : la session a été
ouverte avant l'installation des agents, qui ne se chargent qu'au démarrage. Lancer alors
`subagent_type: "general-purpose"` avec le corps de `~/.claude/agents/plan-reviewer.md` collé en
tête du prompt, même `model`. Idem pour `plan-synthesizer` à l'étape 4.

## Étape 3 — Attendre les trois

Attendre les trois rendus. **Codex indisponible** — binaire absent, authentification manquante,
code de retour non nul, `review-codex.md` vide ou sans `## Verdict`. Si `codex-err.txt` porte un
400 qui nomme le modèle, sonder une fois un autre identifiant (`echo OK | codex exec -m <id> -`)
et relancer avec lui ; sinon, ou si la relance échoue, poursuivre à deux voix en transmettant à
la synthèse le nom de la voix absente et la commande qui a échoué. Ne rien installer sans
demander.

Un relecteur Claude dont le fichier de sortie manque ou n'ouvre pas par `## Verdict` : le
relancer une fois, puis poursuivre sans lui en le signalant de la même façon.

## Étape 4 — Synthèse

`Agent`, `subagent_type: "plan-synthesizer"`. Le prompt contient : le chemin du plan, la racine,
les chemins des revues disponibles, la ou les voix absentes avec la raison, la liste des fichiers
cités non embarqués pour Codex, le cadre verbatim, le chemin de sortie `$SC/synthesis.md`.
Attendre son retour, puis lire `$SC/synthesis.md`.

## Étape 5 — Présenter et trancher

1. Afficher la synthèse telle quelle — ses six sections, sans les reformuler ni les résumer :
   verdict global, convergence, divergences challengées, angles morts, apport propre de chaque
   voix, amendements proposés. La voix absente, s'il y en a une, se lit en tête.
2. `AskUserQuestion` en multi-sélection sur les amendements proposés, **P1 d'abord**, par lots de
   quatre au plus, chaque option citant l'ID de l'amendement et les constats d'origine.
3. Appliquer les amendements retenus au fichier de plan — en mode plan, c'est la seule écriture
   autorisée. Puis ajouter en fin de plan :

```markdown
## Revue de plan
- Date : <AAAA-MM-JJ>
- Voix : <liste> — absente : <voix et raison, ou aucune>
- Verdict global : <décision>
- Appliqués : <n° d'amendement (IDs de constats)>, …
- Écartés : <n° d'amendement (IDs)> — <raison donnée par l'utilisateur, ou « sans motif »>
- Le texte ci-dessus est le plan **amendé après** cette revue ; le verdict porte sur la version
  relue. Relancer `/open-plan-review` pour relire le plan amendé.
```

Dès qu'un amendement P1 ou P2 est appliqué, le dire à l'utilisateur : le plan qu'il va exécuter
n'est plus celui qui a été jugé.

Cette section est une annexe du plan, pas de l'intention : un outil qui extrait l'intention d'un
plan doit l'exclure.
