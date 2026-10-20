#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-codex-prompt.py")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run(plan, frame, repo, budget_kb):
    out = subprocess.run([sys.executable, SCRIPT, "--plan", plan, "--frame", frame,
                          "--repo", repo, "--budget-kb", str(budget_kb)],
                         capture_output=True, check=True)
    return out.stdout.decode("utf-8").replace("\r\n", "\n")


def main():
    checks = 0
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        write(os.path.join(repo, "src", "a.py"), "print('a → ≥ ✓')\n")
        write(os.path.join(repo, "docs", "big.md"), "x" * 4000 + "\n")
        frame = os.path.join(tmp, "frame.md")
        write(frame, "## Verdict\n- Décision : GO\n")
        plan = os.path.join(tmp, "plan.md")
        abs_a = os.path.join(repo, "src", "a.py")
        abs_out = os.path.join(tmp, "elsewhere", "z.md")
        write(plan, "# Plan\n\nModifier `src/a.py` puis `src/missing.py`, voir `docs/big.md` "
                    "et https://example.com/x.md ; relire `./src/a.py`, `~/.claude/plans/p.md`, "
                    f"`$SC/review.md`, `{abs_a}` et `{abs_out}`.\n")

        out = run(plan, frame, repo, budget_kb=3)
        assert "===== CADRE =====" in out and "## Verdict" in out; checks += 1
        assert "===== PLAN : " in out and "    1  # Plan" in out; checks += 1
        assert "===== FICHIER : src/a.py =====" in out and "→ ≥ ✓" in out; checks += 1
        assert out.count("===== FICHIER : src/a.py") == 1; checks += 1
        assert "  - src/missing.py (inexistant)" in out; checks += 1
        assert "  - docs/big.md (budget)" in out and "===== FICHIER : docs/big.md" not in out; checks += 1
        assert "example.com/x.md (inexistant)" not in out; checks += 1
        assert "plans/p.md" not in out.split("===== CADRE")[0]; checks += 1
        assert "SC/review.md" not in out.split("===== CADRE")[0]; checks += 1
        assert f"  - {abs_out.replace(chr(92), '/')} (hors dépôt)" in out; checks += 1
        assert "Fichiers de conventions embarqués : aucun" in out; checks += 1
        assert "===== CONVENTIONS" not in out; checks += 1

        write(os.path.join(repo, "CLAUDE.md"), "# Règles\n")
        out = run(plan, frame, repo, budget_kb=150)
        assert "Fichiers de conventions embarqués : CLAUDE.md" in out; checks += 1
        assert "===== CONVENTIONS : CLAUDE.md =====" in out and "    1  # Règles" in out; checks += 1
        assert "===== FICHIER : docs/big.md =====" in out; checks += 1
        assert "Fichiers cités non embarqués : \n  - " in out and "  - src/missing.py (inexistant)" in out; checks += 1
        assert "  - src/a.py" not in out; checks += 1
    print(f"OK — {checks} vérifications")


if __name__ == "__main__":
    main()
