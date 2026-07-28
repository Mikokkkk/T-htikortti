# Analysis framework: from voice dictation to WANT and NEED

Dictation is thinking out loud. It contains the raw intent, but wrapped in
tangents, restarts, corrections, and filler. This framework turns that into a
plan. Two questions drive everything:

- **WANT** — what is the user trying to achieve? (the destination)
- **NEED** — what must actually happen to get there? (the route)

Most of the leverage is in doing NEED well: the user voiced the WANT; your value
is making the unspoken requirements explicit.

---

## Step 1 — Clean and segment

- Read all transcripts in chronological order. Order reveals evolution of
  thinking.
- Drop noise: unrelated messages, one-word fragments, dictation clearly meant for
  something else (a text to a friend, a Slack quip).
- Split long ramblings into discrete "thought units" — one idea each.

## Step 2 — Cluster into projects/themes

- Group thought units that concern the same initiative.
- A single dictation session can touch several projects; a single project can
  span many sessions. Cluster by topic, not by timestamp.
- If the user asked for one plan, pick the dominant cluster and note what you set
  aside. If they asked for several, keep clusters separate.

## Step 3 — Resolve contradictions and evolution

- People revise mid-thought: "let's use Postgres... actually no, SQLite is
  fine." Later statements usually win.
- Distinguish a *decision changed* (take the latest) from a *genuine open
  question* (the user never settled it → flag it).
- Never silently average two conflicting statements into a mushy middle.

## Step 4 — Extract the WANT

Produce a structured brief:

| Field | What to capture |
|---|---|
| Project name | Crisp, specific title |
| One-line summary | The whole thing in a sentence |
| Goal / end state | What "done and good" looks like |
| Why it matters | Motivation, if voiced |
| In scope | What's explicitly included |
| Out of scope | What the user said to defer or exclude |
| Constraints | Stack, tools, deadline, budget, style |
| Success criteria | How we'll know it worked |

If a field wasn't voiced, write "not specified" rather than inventing it. The
gaps become open questions.

## Step 5 — Derive the NEED

For the WANT, reason from goal backward to the work:

1. **Decompose** into workstreams → tasks. Each task = one focused unit of work.
2. **Add the implicit.** Dictation gives goals, not mechanics. Supply the
   unspoken-but-required steps: environment setup, data/schema, auth, error
   handling, testing, deployment, documentation, edge cases.
3. **Sequence** by dependency. Identify what blocks what.
4. **Assign executability.** For each task: objective, approach, acceptance
   criteria, inputs/dependencies, suggested agent or skill.
5. **Estimate roughly** (S/M/L or hours) if the user wants planning signal.

## Step 6 — Separate the known from the assumed

Three explicit buckets, always:

- **Decided** — clearly stated by the user; execute as-is.
- **Assumed** — you inferred it to fill a gap; state the assumption so it can be
  corrected.
- **Open question** — genuinely unresolved; the user must decide before or during
  execution.

Hiding an assumption as if it were a decision is the most damaging failure mode —
it produces confident, wrong plans. Surface everything.

---

## Guiding principles

- **Faithful, not creative.** Represent what the user wants, not what you'd want.
- **Concrete beats complete.** A sharp plan for the core beats a vague plan for
  everything.
- **Traceability.** Tie key requirements back to the actual dictation so intent
  is auditable.
- **Agent-first phrasing.** Assume the reader is an AI agent with no context.
  Every instruction must survive being read cold.
