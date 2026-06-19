#!/bin/bash
# Hook PreToolUse (Edit|Write) — bloque les modifications sur les fichiers proteges
# Exit 0 = autorise, Exit 2 = bloque (message sur stderr)
# Portee : garde-fou cote agent Claude Code uniquement (defense en profondeur),
# pas une frontiere de securite — n'affecte ni la CI ni un acces FS direct.

INPUT=$(cat)
# Extraire le file_path sans jq (grep + sed)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"\s*:\s*"[^"]*"' | sed 's/"file_path"\s*:\s*"//;s/"$//')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Fichiers generes par NSwag — ne jamais editer manuellement
if echo "$FILE_PATH" | grep -q 'service-proxies\.ts'; then
  echo "Bloque: service-proxies.ts est genere par NSwag. Utilise 'cd nswag && refresh.bat'." >&2
  exit 2
fi

# Migrations EF Core existantes — ne jamais modifier apres commit
if echo "$FILE_PATH" | grep -q 'Infrastructure/Persistence/Migrations/'; then
  echo "Bloque: les migrations EF Core existantes ne doivent pas etre modifiees. Creer une nouvelle migration." >&2
  exit 2
fi

# Fichiers d'environnement sensibles
if echo "$FILE_PATH" | grep -qE '\.env$|\.env\.'; then
  echo "Bloque: fichier .env sensible. Modifier manuellement." >&2
  exit 2
fi

# Fichiers appsettings d'environnement — contiennent des secrets en local.
if echo "$FILE_PATH" | grep -qE 'appsettings\.[^/]+\.json$'; then
  echo "Bloque: appsettings.*.json peut contenir des secrets. Modifier manuellement." >&2
  exit 2
fi

# Lock files
if echo "$FILE_PATH" | grep -qE 'package-lock\.json$'; then
  echo "Bloque: package-lock.json est genere par npm install. Ne pas editer." >&2
  exit 2
fi

exit 0
