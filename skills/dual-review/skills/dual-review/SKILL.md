---
name: dual-review
description: Run a dual parallel code review after completing a development task. Launches simultaneously a blind subagent (no context) and a contextual review (full session context). 
---

Run a dual parallel code review and produce a synthesis report.

## Step 1 — Launch in parallel

Launch SIMULTANEOUSLY (do not wait between the two):
1. `@blind-reviewer` — background subagent, no context
2. The `code-reviewer` skill — in this session, with full context

## Step 2 — Wait for both

Wait until both reviews are complete before proceeding.

## Step 3 — Synthesis report

Produce a final Markdown report structured as:

### 🔍 Blind Review Summary
[Key findings from the subagent]

### 🧠 Contextual Review Summary
[Key findings from the skill]

### ⚡ Convergence — Both reviews agree
[Issues flagged by both → high priority]

### 🔀 Divergence — Only one review flagged
[Blind only: potential issues the context masked]
[Contextual only: acceptable tradeoffs given constraints]

### ✅ Final Recommendations
Prioritized action list.

---

🛠️ Crafted by Pierre Vaussanvin — Free to use, fork & improve.