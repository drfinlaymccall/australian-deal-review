---
description: Run the Australian-side screen - FIRB, ACCC merger notification, takeovers, restraints - against the legislation as at a given date
allowed-tools: ["Read", "Write", "Glob", "Grep", "Skill", "mcp__au-instruments__provision_on_date", "mcp__au-instruments__instrument_on_date", "mcp__au-instruments__what_changed", "mcp__au-instruments__find_in_law"]
---

# Australian-side check

Load the `australian-deal-law` skill and follow it.

$ARGUMENTS may name a date or a document. With no date, run the check at
each of the dates in `deal.md` — draft date, signing, completion, today
— and report where the answers differ. **A difference between those
dates is the finding**, because it means the position changes between
now and completion.

## Report

For each of foreign investment screening, merger notification,
takeovers and restraints:

- whether it is engaged, not engaged, or cannot be determined from what
  is known;
- the provision relied on, quoted, with the date read at and the
  instrument that last changed it;
- what is missing — a fact about the buyer, a look-back figure, an Act
  that is not in this corpus;
- the question for counsel.

End with the things that rest on material **outside** the corpus: the
Acts, and anything about tax. Those are for counsel and the tax adviser,
and must not be answered here.
