# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`ai-shares` is a personal collection of **shareable Claude Code customizations** authored by Pierre Vaussanvin: skills, sub-agents, prompts, and hooks meant to be copied into other projects' `.claude/` directories. The skills are all self-designed; the prompts are a mix of original design and material adapted from others.

There is no build system, no tests, no package manager, and no git here. The artifacts are Markdown (skill/agent definitions, templates, guides) and shell scripts (hooks). "Working in this repo" means editing those definitions — not running an application.

## The single most important thing: repo layout ≠ install layout

The directory structure here is a **distribution/staging layout**. The paths *inside* the files refer to where the artifact lands once installed — almost always under a project's `.claude/`. When you read a file, trust the paths it references over the path it currently sits at.

- `skills/<name>/SKILL.md` here → installs to `.claude/skills/<name>/SKILL.md`
- `skills/<name>/agents/.../foo.agent.md` here → installs to `.claude/agents/.../foo.agent.md`
- `hooks/*.sh` here → installs to `.claude/hooks/*.sh`, wired up in `settings.json`

Some skills bundle the **full install subtree** so a user can copy it verbatim — which is why you'll see apparent doubling like `skills/dual-review/skills/dual-review/SKILL.md` and `skills/dev-notes-writer/agents/dev-notes-writer/dev-notes-writer.agent.md`. The inner path is the real install target; the outer `skills/<name>/` is just the packaging wrapper. Don't "fix" this nesting.

When a skill's `SKILL.md` references a sibling like `references/agent-roles.md` or `assets/briefing-template.md`, those are the *installed* relative paths. In this repo the same files may be flattened (e.g. `skills/taskforce/agent-roles.md`, `skills/taskforce/briefing-template.md`). Keep the in-file references pointing at the install layout.

## Authoring conventions (match these when adding/editing)

- **Skill frontmatter** (`SKILL.md`): `name` + a `description` whose job is *trigger routing* — it enumerates the natural-language phrases and situations that should fire the skill. Write descriptions as discovery surface, not summaries. `taskforce`'s description is the reference example.
- **Agent frontmatter** (`*.agent.md` / agent `.md`): `name`, `description`, and optionally `model` (e.g. `sonnet` to force a cheaper/faster model than the parent session), `tools`, `memory: project`, `background: true`, `skills: [...]`. The `dev-notes-writer` README explains the rationale for choosing an agent over a skill (forced model, isolated context, persistent project memory).
- **Language**: skill/agent bodies are primarily **French**; some prompts and templates are English. Match the language already in the file you're editing.
- **Bundled guides + templates**: heavier instructions live in separate files the skill/agent reads at runtime (`prompts/*.md`, `templates/*.md`, `assets/*.md`, `references/*.md`) rather than inline, so they can evolve independently. Preserve this split.

## Recurring design patterns across the skills

- **Real parallelism for sub-agents**: multi-agent skills (`taskforce`, `dual-review`) insist that all `Task` calls go out **in the same message**. Launching agents in separate messages is treated as a bug ("séquentiel déguisé"). Keep this invariant in any orchestration skill.
- **Incisive, bounded agent prompts**: agent prompts must state identity, mission, **explicit scope including what the agent must NOT handle** (deferring to other agents), named deliverable file path, and a concision constraint. See `skills/taskforce/agent-roles.md` for the canonical templates and anti-patterns.
- **No retroactive fabrication**: `dev-notes-writer` is explicitly forbidden from inventing plausible after-the-fact rationale — it documents only what was actually decided/noted during the session.
- **Dated, structured output dirs**: work products go to predictable paths like `docs/taskforce/` and `docs/dev-notes/YYYY-MM-DD_HHMM_<slug>/`; check whether `docs/` exists before creating, and never overwrite.

## Hooks

`hooks/` holds `PreToolUse` guards (exit 0 = allow, exit 2 = block with a message on stderr). They are jq-free (parse the JSON tool input with `grep`/`sed`) so they run on Windows Git Bash:

- `block-dangerous.sh` — blocks destructive shell/git (`push --force`, `reset --hard`, `checkout .`, `clean -f`, `branch -D`, `rm -rf`); `--force-with-lease` is intentionally allowed.
- `protect-files.sh` — blocks `Edit`/`Write` on generated or secret files (NSwag `service-proxies.ts`, committed EF Core migrations, `.env*`, `appsettings.*.json`, `package-lock.json`).
- `skills/dev-notes-writer/hooks/check-dev-notes-before-commit.{sh,ps1}` — blocks `git commit` unless a dev-note dated today is staged (amends bypass).

These are **defense-in-depth guards for the Claude agent only**, not a security boundary — they don't affect CI or direct filesystem access. Some patterns (the NSwag/EF/appsettings rules) are tailored to a specific downstream project; treat them as templates to adapt, and keep the `.sh`/`.ps1` pair in sync when one exists.
