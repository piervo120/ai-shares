# .claude/hooks/check-dev-notes-before-commit.ps1
# Auto-skip on non-Windows (PowerShell 7+ also runs on Linux/macOS) — the .sh sibling handles those.
if ($IsLinux -or $IsMacOS) { exit 0 }

$payload = [Console]::In.ReadToEnd()

# Match a `git commit` invocation directly in the JSON `command` field.
# Pattern: "command":"[ws][env=val ...]git [-c k=v ...] commit ..."
$commitPattern = '"command"\s*:\s*"\s*([A-Za-z_][A-Za-z0-9_]*=\S+\s+)*git(\s+-c\s+\S+)*\s+commit(\s|")'
if ($payload -notmatch $commitPattern) { exit 0 }

# Amends bypass — dev-note already enforced on the original commit.
if ($payload -match '--amend(\s|"|$|=)') { exit 0 }

$today = Get-Date -Format 'yyyy-MM-dd'
$staged = git diff --cached --name-only | Select-String -Pattern "^docs/dev-notes/${today}_" -Quiet

if (-not $staged) {
    [Console]::Error.WriteLine("Commit bloqué : ce changement nécessite une dev note.")
    [Console]::Error.WriteLine("Délègue à l'agent dev-notes-writer pour générer la documentation, puis 'git add docs/dev-notes/' avant de refaire le commit.")
    exit 2
}

exit 0
