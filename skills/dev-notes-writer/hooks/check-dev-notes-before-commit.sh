#!/bin/bash
# .claude/hooks/check-dev-notes-before-commit.sh
# Runs on all platforms — Git Bash provides grep/git on Windows.

INPUT=$(cat)

# Match a `git commit` invocation directly in the JSON `command` field.
# Pattern: "command":"[ws][env=val ...]git [-c k=v ...] commit ..."
if ! printf '%s' "$INPUT" | grep -qE '"command"[[:space:]]*:[[:space:]]*"[[:space:]]*([A-Za-z_][A-Za-z0-9_]*=[^[:space:]]+[[:space:]]+)*git([[:space:]]+-c[[:space:]]+[^[:space:]]+)*[[:space:]]+commit([[:space:]]|\")'; then
  exit 0
fi

# Amends bypass — dev-note already enforced on the original commit.
if printf '%s' "$INPUT" | grep -qE -- '--amend([[:space:]\"]|$|=)'; then
  exit 0
fi

TODAY=$(date +%Y-%m-%d)
DEV_NOTES_STAGED=$(git diff --cached --name-only | grep -E "^docs/dev-notes/${TODAY}_" || true)

if [ -z "$DEV_NOTES_STAGED" ]; then
  echo "Commit bloqué : ce changement nécessite une dev note." >&2
  echo "Délègue à l'agent dev-notes-writer pour générer la documentation, puis 'git add docs/dev-notes/' avant de refaire le commit." >&2
  exit 2
fi

exit 0
