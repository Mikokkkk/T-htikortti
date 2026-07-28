# Agent-ready project plan template

Fill every section. Keep it Markdown. The reader is an AI agent with NO prior
context — write so it can execute cold. Delete bracketed guidance as you fill in.

---

# Project Plan: <Project Name>

> Generated from Wispr Flow dictation on <date>. Source window: <range>.

## 1. Summary

<One paragraph: what this project is and the desired end state. An agent should
grasp the whole thing from this alone.>

## 2. Goal & success criteria

- **Goal:** <the destination — what "done and good" looks like>
- **Success criteria:**
  - [ ] <measurable, verifiable outcome>
  - [ ] <measurable, verifiable outcome>

## 3. Scope

- **In scope:** <what this project covers>
- **Out of scope:** <what to explicitly NOT do / defer>

## 4. Context & constraints

- **Stack / tools:** <languages, frameworks, services required>
- **Access needed:** <repos, APIs, files, accounts the executing agent needs>
- **Constraints:** <deadlines, budget, style, compliance, anything stated>

## 5. Assumptions & open questions

> Be honest here. Do not bury guesses inside tasks.

- **Assumptions** (inferred to fill gaps — correct if wrong):
  - <assumption>
- **Open questions** (need a human decision):
  - <question — and why it matters / what's blocked until answered>

## 6. Workstreams & tasks

> Order tasks by dependency. Each task is a self-contained unit an agent can be
> handed directly. Give each a stable ID (T1, T2, …).

### Workstream A: <name>

#### T1 — <task title>
- **Objective:** <what this task achieves, one line>
- **Steps / approach:** <concrete how — specific enough to act on>
- **Inputs / dependencies:** <files, data, prior tasks (e.g. "after T0")>
- **Acceptance criteria:** <how the agent verifies it's done and correct>
- **Suggested agent/skill:** <optional — who should run this>
- **Est.:** <S / M / L, optional>
- **Source:** <quote or paraphrase of the dictation this came from>

#### T2 — <task title>
- ...

### Workstream B: <name>
- ...

## 7. Execution order

<Linear or dependency-ordered list of task IDs, e.g. T1 → T2 → (T3, T4 parallel)
→ T5. This is the sequence an orchestrator should follow.>

## 8. Deliverables

- <artifact the project produces, and where it should land>

## 9. Handoff notes

<Anything an executing agent should know: gotchas, preferences, things the user
cares about, how to report back.>
