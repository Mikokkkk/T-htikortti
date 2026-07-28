---
name: wispr-flow-project-plan
description: >-
  Turn Wispr Flow voice dictation into agent-ready project plans. Use when the
  user wants to pull their Wispr Flow transcripts and convert spoken thoughts
  into a concrete project plan, spec, or task breakdown they can hand to AI
  agents. Triggers include: "wispr flow", "my dictations", "my transcripts",
  "turn what I said into a plan", "make a project plan from my voice notes",
  "build a spec from my Wispr transcripts".
---

# Wispr Flow → Project Plan

Convert rambling voice dictation captured in Wispr Flow into a clear, concrete,
AGENT-READY project plan (Markdown). The pipeline runs in four stages:

1. **PULL** — extract transcripts from the local Wispr Flow database.
2. **UNDERSTAND (WANT)** — figure out what the project is and what the user
   wants to achieve.
3. **DERIVE (NEED)** — work out what must actually be done to get there.
4. **PLAN** — write the sharpest possible agent-ready project plan.

The whole point: another AI agent should be able to pick up the output plan and
execute it with no further context. Optimize every stage for that.

---

## Stage 0 — Scope the request (ask first)

Before pulling anything, confirm scope in ONE short round of questions unless the
user already gave it:

- **Time window** — last day / week / month / a specific date range? (default:
  last 7 days)
- **One project or several?** — Is this one project buried in the dictations, or
  should you split the transcripts into multiple project plans?
- **Filter** — any keyword or source app that isolates the relevant dictations?
  (e.g. only transcripts mentioning "the API rewrite")

Keep it to the essentials. Then proceed.

---

## Stage 1 — PULL transcripts

Run the extraction script. It reads Wispr Flow's local SQLite database
(`flow.sqlite`), which contains every dictation. Nothing leaves the machine.

```bash
python3 scripts/pull_transcripts.py --since 7d --out ./wispr_bundle
```

Common options:

- `--since 7d` / `48h` / `30m` — relative window
- `--from 2026-07-01 --to 2026-07-23` — explicit range
- `--contains "onboarding"` — only transcripts containing text
- `--app Slack` — only dictations made into a given app
- `--min-words 10` — drop tiny fragments (good default: 8–12)
- `--db /path/to/flow.sqlite` — override auto-detection

**Auto-detected DB locations:**
- macOS: `~/Library/Application Support/Wispr Flow/flow.sqlite`
- Windows: `%APPDATA%\Wispr Flow\flow.sqlite`

The script writes `transcripts.json` (structured) and `transcripts.md` (readable)
to the output dir. **Read `transcripts.json`** — it is the raw material for every
later stage.

**If the script fails:**
- "Could not find flow.sqlite" → ask the user for the path, or have them confirm
  Wispr Flow is installed with local history on. On Windows the folder is
  `%APPDATA%\Wispr Flow`.
- DB locked → the script auto-copies the file; if it still fails, ask the user to
  quit Wispr Flow and retry.
- 0 transcripts → loosen `--since` / `--min-words` / `--contains`.
- No folder access in this session → ask the user to paste transcript text
  directly, then skip to Stage 2 using the pasted text.

> Note: Wispr Flow has no public cloud API. Reading the local database is the
> supported way to pull history in bulk. This is read-only.

---

## Stage 2 — UNDERSTAND: what is the project, and what do we WANT?

Dictation is messy: half-formed thoughts, tangents, corrections, repetition. Your
job is to distill signal. Read `reference/analysis_framework.md` for the full
method. In short:

1. **Segment & cluster.** Group transcripts that belong to the same project or
   theme. Ignore unrelated dictation (a Slack reply about lunch is noise).
2. **Resolve contradictions.** People change their mind mid-dictation. Later
   statements usually override earlier ones — but flag genuine open questions
   rather than silently picking one.
3. **Extract the WANT**, structured as:
   - **Project name** — a crisp title.
   - **One-line summary** — what this is, in a sentence.
   - **Goal / desired end state** — what "done and good" looks like.
   - **Why it matters** — the motivation, if voiced.
   - **Scope boundaries** — what's explicitly IN and OUT (dictation often says
     "I don't want to deal with X yet" — capture that).
   - **Constraints & preferences** — tools, deadlines, stack, style, budget,
     anything stated.
   - **Success criteria** — how we'll know it worked.

Write this up as a short **Project Brief**. Show it to the user and confirm you
understood the WANT before building the full plan. This checkpoint matters:
everything downstream inherits errors made here.

---

## Stage 3 — DERIVE: what do we NEED to do?

Now translate intent into execution. WANT is the destination; NEED is the route.
For the confirmed brief, reason out:

1. **Decompose into workstreams**, then into concrete tasks. Each task must be
   small enough for one agent to complete in one focused pass.
2. **Surface the implicit.** Dictation states goals, not mechanics. YOU add the
   unspoken-but-required work: setup, data, auth, testing, deployment, docs,
   edge cases. This is where most of the value is — the user said the WANT;
   you're supplying the NEED they didn't spell out.
3. **Order by dependency.** What must exist before what? Mark blockers.
4. **Flag decisions & unknowns.** Anywhere the transcripts left a gap, make it an
   explicit open question or a stated assumption — never a silent guess.
5. **Make each task agent-executable.** For every task capture: a clear
   objective, concrete steps or approach, acceptance criteria (how an agent
   verifies it's done), inputs/dependencies, and — where useful — a suggested
   agent or skill to run it.

If the request implies external tools (a repo, Figma, Slack, a database, a
deploy target), note them so the executing agent knows what it needs access to.

---

## Stage 4 — PLAN: write the agent-ready document

Build the plan using `reference/plan_template.md`. Write it to the output folder
as Markdown, e.g. `PROJECT_PLAN_<slug>.md`.

Quality bar — the plan must be:

- **Self-contained.** An agent with zero prior context can execute it.
- **Concrete.** No vague verbs ("improve", "handle"). Say exactly what and how.
- **Verifiable.** Every task has acceptance criteria.
- **Traceable.** Key requirements link back to what the user actually said
  (quote or paraphrase the source dictation) so intent is auditable.
- **Honest about gaps.** Open questions and assumptions are listed, not hidden.

Every task should be phrased as a discrete unit of work an agent can be handed
directly — objective, steps, acceptance criteria, dependencies.

If the user asked for multiple projects, produce one plan file per project.

After writing, present the file(s) and give a 2–3 sentence summary plus any open
questions the user should resolve. Offer to split any task block into a
standalone prompt they can paste to an agent.

---

## Optional: keep it running

If the user wants this regularly ("every Friday turn my week's dictations into a
plan"), offer to set up a scheduled task that runs the pull + plan pipeline on a
cadence.

## Files

- `scripts/pull_transcripts.py` — local DB extractor (stdlib only).
- `reference/analysis_framework.md` — WANT vs NEED distillation method.
- `reference/plan_template.md` — the agent-ready plan structure.
