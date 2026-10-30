---
description: Review a new draft from the buyer - redline, playbook grading, Australian checks, issues update, counsel pack
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill", "mcp__au-instruments__provision_on_date", "mcp__au-instruments__instrument_on_date", "mcp__au-instruments__what_changed", "mcp__au-instruments__find_in_law"]
---

# Review this turn

The routine that runs on every new draft. Load the
`earnout-review` skill and follow it; load `australian-deal-law` for
step 3.

$ARGUMENTS names the new draft. If nothing was given, find the most
recent file in the deal folder and say which one you picked.

## Do this

1. Read `playbook.md`, `issues.md`, `deal.md` and the previous turn in
   `turns/`. If the playbook is still empty, grade nothing — describe
   the clauses and say plainly that grading needs counsel's playbook.
2. Run `what_changed` on every instrument, from the previous turn's date
   to today. The law can move between turns without the draft changing.
3. Work the six steps in the `earnout-review` skill, in order.
4. Write the result to `turns/NN-YYYY-MM-DD.md` and update `issues.md`
   in place.

## Output

In the chat, give only:

- the **red lines** found, with the clause quoted;
- what **moved** since the last turn, including anything in the law;
- the **counsel pack** — the flagged items only;
- what you **could not check**, and why.

Everything else belongs in the turn file. Do not draft anything to the
buyer.
