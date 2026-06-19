#!/bin/bash
# Hook PreToolUse (Bash) — bloque les commandes git/shell destructives
# Exit 0 = autorise, Exit 2 = bloque (message sur stderr)
# Portee : garde-fou cote agent Claude Code uniquement (defense en profondeur),
# pas une frontiere de securite — n'affecte ni la CI ni un acces FS direct.

INPUT=$(cat)
# Extraire la commande sans jq (grep + sed)
COMMAND=$(echo "$INPUT" | grep -o '"command"\s*:\s*"[^"]*"' | sed 's/"command"\s*:\s*"//;s/"$//')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Patterns dangereux (insensible a la casse)
# --force-with-lease est sur (refuse si le remote a bouge) -> autorise.
if echo "$COMMAND" | grep -qiE 'git\s+push\s+.*(--force(\s|$)|-f(\s|$))'; then
  echo "Bloque: git push --force/-f. Utilise --force-with-lease si necessaire." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qiE 'git\s+reset\s+--hard'; then
  echo "Bloque: git reset --hard. Utilise git stash ou git reset --soft." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qiE 'git\s+checkout\s+(\.|--\s*\.)'; then
  echo "Bloque: git checkout . (ecrase les modifications locales). Utilise git stash." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qiE 'git\s+clean\s+-[a-zA-Z]*f'; then
  echo "Bloque: git clean -f (supprime les fichiers non suivis). Trop destructif." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qiE 'git\s+branch\s+-D'; then
  echo "Bloque: git branch -D (suppression forcee). Utilise git branch -d." >&2
  exit 2
fi

if echo "$COMMAND" | grep -qiE 'rm\s+-[a-zA-Z]*r[a-zA-Z]*f|rm\s+-[a-zA-Z]*f[a-zA-Z]*r'; then
  echo "Bloque: rm -rf. Trop destructif — supprime les fichiers un par un." >&2
  exit 2
fi

exit 0
