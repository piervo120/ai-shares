#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-codex-prompt.py")


def write(path, text, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    kwargs = {} if "b" in mode else {"encoding": "utf-8"}
    with open(path, mode, **kwargs) as f:
        f.write(text)


def run(brief, rubric, repo, files, budget_kb=150, env=None):
    return subprocess.run([sys.executable, SCRIPT, "--brief", brief, "--rubric", rubric,
                           "--repo", repo, "--budget-kb", str(budget_kb), "--files", *files],
                          capture_output=True, env=env)


def text(proc):
    return proc.stdout.decode("utf-8").replace("\r\n", "\n")


def main():
    checks = 0
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "repo")
        write(os.path.join(repo, "src", "a.py"), "print('a → ≥ ✓')\n")
        write(os.path.join(repo, "docs", "big.md"), "x" * 4000 + "\n")
        write(os.path.join(repo, "img", "logo.bin"), b"\x00\x01\x02", mode="wb")
        brief = os.path.join(tmp, "brief.md")
        write(brief, "Le lot doit garantir que a ≥ b.\n")
        rubric = os.path.join(tmp, "rubric.md")
        write(rubric, "## Axes\n- [P1] défaut réel\n")
        files = ["src/a.py", "src/missing.py", "docs/big.md", "img/logo.bin", "src/a.py"]

        legacy_console = dict(os.environ, PYTHONIOENCODING="cp1252")
        legacy_console.pop("PYTHONUTF8", None)
        proc = run(brief, rubric, repo, files, budget_kb=3, env=legacy_console)
        assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace"); checks += 1
        out = text(proc)
        assert "===== GRILLE =====" in out and "défaut réel" in out; checks += 1
        assert "===== BRIEF D'INTENTION =====" in out and "a ≥ b" in out; checks += 1
        assert "===== FICHIER : src/a.py =====" in out and "→ ≥ ✓" in out; checks += 1
        assert "    1  print('a" in out; checks += 1
        assert out.count("===== FICHIER : src/a.py") == 1; checks += 1
        assert "  - src/missing.py (inexistant)" in out; checks += 1
        assert "  - docs/big.md (budget)" in out and "===== FICHIER : docs/big.md" not in out; checks += 1
        assert "  - img/logo.bin (binaire)" in out; checks += 1
        assert "Fichiers du lot non embarqués : \n  - " in out; checks += 1

        out = text(run(brief, rubric, repo, ["src/a.py", "docs/big.md"]))
        assert "Fichiers du lot non embarqués : aucun" in out; checks += 1
        assert "===== FICHIER : docs/big.md =====" in out; checks += 1

        proc = run(brief, rubric, repo, ["src/missing.py", "img/logo.bin"])
        assert proc.returncode != 0 and proc.stdout == b""; checks += 1
        assert b"src/missing.py (inexistant)" in proc.stderr; checks += 1

        list_file = os.path.join(tmp, "files.txt")
        write(list_file, "src/a.py\n\ndocs/big.md\n")
        proc = subprocess.run([sys.executable, SCRIPT, "--brief", brief, "--rubric", rubric,
                               "--repo", repo, "--files-from", list_file], capture_output=True)
        out = text(proc)
        assert "===== FICHIER : src/a.py =====" in out and "===== FICHIER : docs/big.md =====" in out; checks += 1
    print(f"OK — {checks} vérifications")


if __name__ == "__main__":
    main()
