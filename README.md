# australian-deal-review

A Claude Code plugin for reviewing deal documents turn by turn, with
the Australian-side checks read from the legislation **as it stood on
the date that matters** rather than from memory. It goes deepest on the
earn-out, which is the part most often argued about afterwards.

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

There is nothing hosted behind this plugin and no API key to get. The
legislation tools come from an MCP server you run yourself, on your own
machine, out of a clone of the corpus it reads. Setting it up is two
steps — get the corpus, then tell the plugin where you put it — and the
rest of this section is checking that it answers.

### 1. Get the corpus, which carries the server

```bash
git clone https://github.com/drfinlaymccall/australia-instruments.git
```

About 35 MB on disk. The server is `tools/mcp_server.py` inside that
clone: Python 3.11 or later and `git`, standard library only, nothing to
install. It speaks MCP over stdio, answers from the clone's git history,
and makes no network calls.

The plugin runs that copy rather than shipping one of its own. There is
one implementation of the reader and it lives with the record it reads,
so a correction to it arrives with a `git pull` in the corpus rather
than with a new release of this plugin. Two copies of a reader of a
legal record drift, and the drift is silent.

If you would rather not take the published history on trust, build the
corpus yourself from the Federal Register of Legislation — `Building it`
in the corpus README gives the four commands — and point the plugin at
your build instead. It cannot tell the difference.

### 2. Tell the plugin where it is

```bash
export AU_INSTRUMENTS_CORPUS=/path/to/australia-instruments
```

Put the `export` in your shell profile so it survives a new terminal,
and start Claude Code from a shell that has it. Nothing works without
it: the variable is both where the law is and where the reader is.

### 3. Install the plugin

```
/plugin install australian-deal-review --marketplace drfinlaymccall/australian-deal-review
```

### 4. Check that it answers

Run `/deal-setup` in the folder holding the deal documents. Before it
creates anything it asks the corpus for an instrument at today's date,
and if that fails it says exactly what is wrong rather than carrying on
and answering Australian questions from memory. The usual cause is step
2: the variable is unset, misspelled, or set in a different shell from
the one Claude Code is running in.

To exercise the server on its own, without this plugin:

```bash
cd /path/to/australia-instruments
claude mcp add au-instruments -- python3 -I tools/mcp_server.py
```

Then ask it what the combined acquirer/target revenue test was on
1 January 2026, and which instrument set that figure.

### 5. Get the playbook filled in by counsel

This is the step that makes the rest worth having: it is how counsel's
judgement gets applied on every turn without being paid for again. Until
it is filled in, reviews describe clauses but do not grade them, and say
so.

### Where the legislation tools run

A local MCP server is started by the app that loads the plugin, so the
Australian checks are only available where that can happen:

| | Legislation tools |
| --- | --- |
| Claude Code | Yes |
| Cowork | Only when the session runs on your own computer |
| claude.ai chat | No — local MCP servers are ignored there |

The skills and commands load everywhere, but without the server the
Australian checks have nothing to read. Use this in Claude Code.

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
