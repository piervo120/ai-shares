#!/usr/bin/env python3
"""Assemble le prompt Codex d'une relecture de plan : cadre, plan, conventions du projet,
fichiers cités par le plan — le tout embarqué, sous budget, avec la liste de ce qui a été écarté."""
import argparse
import os
import re
import subprocess
import sys

CONVENTION_FILES = ("CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md")
PATH_RE = re.compile(r"(?:[A-Za-z]:[\\/])?[\w.~$][\w./\\-]*\.\w{1,6}")


def repo_root(explicit):
    if explicit:
        return os.path.abspath(explicit)
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, check=True).stdout.strip()
        if out:
            return os.path.abspath(out)
    except (OSError, subprocess.CalledProcessError):
        pass
    return os.getcwd()


def cited_paths(text, root):
    seen = []
    outside = []
    for m in PATH_RE.finditer(text):
        p = m.group(0)
        if "/" not in p and "\\" not in p:
            continue
        if p[0] in "~$" or text[max(0, m.start() - 3):m.start()].endswith(("://", ":/")):
            continue
        p = p.replace("\\", "/")
        if p.startswith("./"):
            p = p[2:]
        if os.path.isabs(p):
            rel = os.path.relpath(os.path.abspath(p), root).replace("\\", "/")
            if rel.startswith(".."):
                if p not in outside:
                    outside.append(p)
                continue
            p = rel
        if p not in seen:
            seen.append(p)
    return seen, outside


def numbered(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    return "\n".join(f"{i:5d}  {l}" for i, l in enumerate(lines, 1))


def size(s):
    return len(s.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--frame", required=True)
    ap.add_argument("--repo")
    ap.add_argument("--budget-kb", type=int, default=150)
    ap.add_argument("--prefix", default="CX-")
    args = ap.parse_args()

    root = repo_root(args.repo)
    budget = args.budget_kb * 1024
    frame = open(args.frame, encoding="utf-8").read()
    plan_text = open(args.plan, encoding="utf-8").read()

    parts = [f"\n===== CADRE =====\n{frame}",
             f"\n===== PLAN : {args.plan} =====\n{numbered(args.plan)}"]
    used = sum(size(p) for p in parts)

    conventions = []
    for name in CONVENTION_FILES:
        path = os.path.join(root, name)
        if os.path.isfile(path):
            block = f"\n===== CONVENTIONS : {name} =====\n{numbered(path)}"
            parts.append(block)
            used += size(block)
            conventions.append(name)

    cited, outside = cited_paths(plan_text, root)
    skipped = [(p, "hors dépôt") for p in outside]
    for rel in cited:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            skipped.append((rel, "inexistant"))
            continue
        block = f"\n===== FICHIER : {rel} =====\n{numbered(path)}"
        if used + size(block) > budget:
            skipped.append((rel, "budget"))
            continue
        parts.append(block)
        used += size(block)

    sys.stdout.reconfigure(encoding="utf-8")
    print("N'EXÉCUTE AUCUNE COMMANDE ET NE LIS AUCUN FICHIER. Tout ce qui est à relire est embarqué ci-dessous.")
    print("Tu relis un PLAN d'implémentation, pas du code : le code embarqué sert à vérifier ce que le plan affirme.")
    print(f"Ton préfixe d'identifiant est {args.prefix}. Rends ta revue exactement au cadre ci-dessous, en français, sans préambule.")
    print(f"Racine du dépôt : {root}")
    print("Fichiers de conventions embarqués : " + (", ".join(conventions) if conventions else "aucun"))
    print("Fichiers cités non embarqués : " + ("" if skipped else "aucun"))
    for rel, why in skipped:
        print(f"  - {rel} ({why})")
    for p in parts:
        print(p)


if __name__ == "__main__":
    main()
