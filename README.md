# earnout-war-room

A Claude Code plugin for reviewing earn-out drafts turn by turn, with
the Australian-side checks read from the legislation **as it stood on
the date that matters** rather than from memory.

It is preparation for counsel. It does not give legal or tax advice,
and it does not draft anything to the other side.

## Why

An earn-out is the part of a sale price most likely to be argued about
afterwards, and the protection is whatever the contract says expressly.
Reviewing each new draft against a fixed standard is exactly the work
that is valuable, repetitive, and easy to do unevenly at eleven at
night on the fourth turn.

The Australian side is the other half. Where a US buyer's counsel runs
the US position, foreign investment screening, merger notification and
restraints are a different regulator and a different statute — and
since 1 January 2026, a merger regime most precedent documents were not
drafted against. Those thresholds are in legislative instruments that
are amended often. This plugin reads them from the instrument itself,
at a date, and quotes them.

## What it does

| Command | What it does |
| --- | --- |
| `/deal-setup` | Creates the playbook, issues register and scenario model; records the NDA and privilege position; proves the legislation lookup works |
| `/turn-review` | The per-turn routine on a new draft: redline, playbook grading, Australian check, issues update, loop detection, counsel pack |
| `/australia-check` | Foreign investment, merger notification, takeovers and restraints, at each of the deal's dates |
| `/stress-test` | Models the payout under hostile scenarios and ranks the drafting asks by what they are worth |

Two skills carry the substance — `earnout-review` (where the money
leaks, and the per-turn routine) and `australian-deal-law` (the
Australian checks and the limits of the corpus). Claude loads them
itself when the work calls for them.

## Setup

1. **Clone the legislation corpus** and point the plugin at it:

   ```bash
   git clone https://github.com/drfinlaymccall/australia-instruments.git
   export AU_INSTRUMENTS_CORPUS=/path/to/australia-instruments
   ```

   Put the `export` in your shell profile so it survives a new terminal.
   Nothing works without it, and `/deal-setup` checks it before you
   rely on it. A corpus built from source on your own machine works the
   same way: the plugin only ever reads a local clone, never the network.

2. **Install the plugin** into Claude Code, then run `/deal-setup` in
   the folder holding the deal documents.

3. **Get the playbook filled in by counsel.** This is the step that
   makes the rest worth having: it is how counsel's judgement gets
   applied on every turn without being paid for again. Until it is
   filled in, reviews describe clauses but do not grade them, and say
   so.

Python 3.11 or later, standard library only. No API keys, and nothing
leaves the machine: the legislation server reads a local git clone.

## What it is not

- **Not legal or tax advice.** Senior M&A counsel and the Australian
  tax adviser make every call; this produces their inputs and a short
  pack of only the flagged items.
- **Not a complete statement of Australian law.** The corpus holds
  legislative *instruments* — the regulations and determinations that
  carry the thresholds and exemptions — not the Acts they are made
  under, and no tax legislation at all. The `australian-deal-law`
  skill lists exactly what is in and out, and every output is required
  to say when a point rests on something outside it.
- **Not a drafting tool.** It will not write to the buyer unless
  explicitly told to.

## Confidentiality

This plugin contains no deal information. Everything specific to a
transaction lives in files you create in your own working folder —
`playbook.md`, `issues.md`, `deal.md`, `turns/` — and none of it is part
of the plugin. That is deliberate: the plugin can be shared or
installed anywhere without carrying a deal with it.

Before putting deal documents into any AI tool, confirm the NDA permits
it and ask counsel how it affects privilege. `/deal-setup` records both
answers; it cannot give them.

## Licence

Apache-2.0.
