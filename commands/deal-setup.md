---
description: Stand up the deal war room - playbook, issues register, guardrail checks and a corpus connection test
allowed-tools: ["Read", "Write", "Glob", "Bash", "AskUserQuestion", "Skill", "mcp__au-instruments__instrument_on_date"]
---

# Set up the war room

Run once, at the start. It creates the files the other commands rely on
and proves the legislation lookup actually works before anyone depends
on it.

## 1. Check the guardrails first

Before any deal document is read, ask and record the answers in
`guardrails.md`. These are the two questions people skip and regret:

- **NDA.** Does it permit deal documents to be put into AI tools and
  their model providers? Who confirmed, and when?
- **Privilege.** Has counsel been asked how putting their advice into
  third-party tools affects privilege, and how they want it handled?

If either is unanswered, write "not yet confirmed" with the date and
say so once in the first review. Do not block the work on it and do not
raise it every turn — record it and move on.

## 2. Prove the corpus connection

Call `instrument_on_date` for the Foreign Acquisitions and Takeovers
Regulation 2015 at today's date. If it errors, the environment variable
`AU_INSTRUMENTS_CORPUS` is not pointing at a clone of the corpus; say
exactly that and how to fix it, rather than carrying on and quietly
answering Australian questions from memory.

## 3. Create the working files

From `templates/`, if they do not already exist:

- `playbook.md` — **counsel fills this in.** Until they do, reviews are
  ungraded. Say so when you create it.
- `issues.md` — the live issues register.
- `scenarios.md` — the earn-out stress-test model.
- `turns/` — one file per draft received, named `turns/NN-YYYY-MM-DD.md`.

## 4. Record the deal's dates

In `deal.md`: the date of the current draft, the expected signing date,
the expected completion date, and the earn-out period. Every Australian
check is asked at a date, and these are the dates.

## 5. Report

A short summary: what was created, what is missing (the playbook,
usually), whether the corpus answered, and the single next action —
which is almost always "ask counsel for the playbook".
