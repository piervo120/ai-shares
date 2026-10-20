#!/usr/bin/env python3
"""Assemble le prompt Codex d'une revue de code : consigne, grille, brief d'intention, puis les
fichiers du lot numérotés — le tout embarqué, sous budget, avec la liste de ce qui a été écarté."""
import argparse
import os
import subprocess
import sys


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


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def is_binary(path):
    with open(path, "rb") as f:
        return b"\0" in f.read(8192)


def numbered(text):
    return "\n".join(f"{i:5d}  {l}" for i, l in enumerate(text.split("\n"), 1))


def size(s):
    return len(s.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True)
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--files-from")
    ap.add_argument("--repo")
    ap.add_argument("--budget-kb", type=int, default=150)
    args = ap.parse_args()

    root = repo_root(args.repo)
    files = list(args.files)
    if args.files_from:
        files += [l.strip() for l in read_text(args.files_from).splitlines() if l.strip()]

    parts = [f"\n===== GRILLE =====\n{read_text(args.rubric)}",
             f"\n===== BRIEF D'INTENTION =====\n{read_text(args.brief)}"]
    used = sum(size(p) for p in parts)
    budget = args.budget_kb * 1024

    skipped = []
    embedded = 0
    for rel in dict.fromkeys(f.replace("\\", "/") for f in files):
        path = rel if os.path.isabs(rel) else os.path.join(root, rel)
        if not os.path.isfile(path):
            skipped.append((rel, "inexistant"))
            continue
        if is_binary(path):
            skipped.append((rel, "binaire"))
            continue
        block = f"\n===== FICHIER : {rel} =====\n```\n{numbered(read_text(path))}\n```"
        if used + size(block) > budget:
            skipped.append((rel, "budget"))
            continue
        parts.append(block)
        used += size(block)
        embedded += 1

    if embedded == 0:
        print("Aucun fichier embarqué : prompt Codex inutilisable.", file=sys.stderr)
        for rel, why in skipped:
            print(f"  - {rel} ({why})", file=sys.stderr)
        sys.exit(1)

    sys.stdout.reconfigure(encoding="utf-8")
    print("N'EXÉCUTE AUCUNE COMMANDE ET NE LIS AUCUN FICHIER. Tout ce qui est à relire est embarqué ci-dessous.")
    print("Tu relis du CODE contre l'intention du brief : juge-le contre ce que le chantier devait garantir.")
    print("Rends ta revue en français, sans préambule, au format de la grille.")
    print(f"Racine du dépôt : {root}")
    print("Fichiers du lot non embarqués : " + ("" if skipped else "aucun"))
    for rel, why in skipped:
        print(f"  - {rel} ({why})")
    for p in parts:
        print(p)


if __name__ == "__main__":
    main()
