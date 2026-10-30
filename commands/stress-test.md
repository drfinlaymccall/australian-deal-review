---
description: Model the earn-out payout under hostile scenarios to show where the drafting leaks
allowed-tools: ["Read", "Write", "Edit", "Glob", "Bash", "Skill"]
---

# Stress-test the earn-out

Turn the drafting asks into numbers, so they can be prioritised rather
than argued in the abstract. Load the `earnout-review` skill for the
leak routes.

## Build the model

From the current draft, write the earn-out formula into
`scenarios.md` as something computable — a small script or a table, with
every input named and sourced to a clause.

## Run these scenarios

Each one is a way the buyer could lawfully reduce the payout under the
draft as it stands:

- buyer adds X% overhead or management fees
- accounting policy change (revenue recognition, capitalisation)
- a key customer moved to another portfolio company
- the business sold or merged mid-period
- the seller terminated in year 1, and in year 2
- an indemnity claim set off against payment
- the lender blocks payment for one period
- payment delayed past the tax look-through window
- the currency moves 10-15% against the seller

## Report

For each scenario, two numbers: the payout under the **current draft**,
and the payout with the **proposed fix** — after tax, in AUD. Then rank
the fixes by how much they are worth.

State the assumptions. A model whose assumptions are not visible will be
believed more than it deserves, and the tax figures in particular are
illustrative only until the tax adviser has confirmed the treatment.
