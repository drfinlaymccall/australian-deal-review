---
name: earnout-review
description: Review a new draft of an acquisition agreement for the ways an earn-out can be reduced or avoided after closing - calculation, buyer conduct, set-off, lender restrictions, employment - grading each clause against a counsel-approved playbook and producing a short pack of flagged items for counsel. Use when a new draft or redline arrives from the buyer, when asked what changed since the last turn, when asked whether a clause is a red line, or when maintaining the issues register. Preparation for counsel, never advice, and never drafts communications to the buyer unless explicitly told to.
version: 0.1.0
---

# Reviewing an earn-out draft

An earn-out bridges a valuation gap at signing and becomes the thing
most likely to be fought over afterwards. The protection is whatever the
contract says expressly. Courts applying Delaware law read earn-out
terms literally, and implied good faith is weak: in *Lazard Technology
Partners v Qinetiq* (Del. 2015) the seller had to show the buyer acted
**for the purpose of** avoiding the earn-out, which is a very high bar.

So the review question is never "is this fair?". It is: **if the buyer
wanted to pay nothing, what in this draft stops them?**

## Before anything else

Three things must exist, and the review says so plainly if they do not:

1. **The playbook** (`playbook.md`) — counsel's red lines, fallbacks and
   must-haves. Without it, clauses can be described but not graded, and
   the review must say it is ungraded rather than invent a standard.
2. **The issues register** (`issues.md`) — the live list.
3. **The guardrails** — that the NDA permits deal documents to go into
   AI tools, and that counsel has been asked how putting their advice
   into third-party tools affects privilege. If neither is recorded, say
   so once at the top of the first review and carry on; do not keep
   repeating it.

## The per-turn routine

Run these in order for each new draft.

### 1. Redline summary

What changed since the previous turn, in plain English, clause by
clause. Separate the substantive from the cosmetic, and say which
changes were ones **we** asked for and which the buyer introduced
unprompted. A change nobody asked for is worth a second look.

### 2. Playbook deviation check

Every earn-out clause graded **acceptable / needs negotiation / red
line** against the playbook, quoting the exact clause text. Grade
against what the playbook says, not against what seems reasonable. Where
the playbook is silent, say "not covered by the playbook" rather than
guessing — that silence is itself something counsel should know about.

### 3. Australian check

Use the `australian-deal-law` skill. Approvals, conditions, longstop
dates, restraints, governing law and currency, plus anything touching
Australian tax treatment, which goes to the tax adviser rather than
being answered.

### 4. Issues register update

For each open point: owner, our position, their position, proposed
trade, status.

### 5. Loop detection

Any point that has bounced more than twice. Those rarely close on their
own; propose a package or a trade that moves two at once.

### 6. Counsel pack

A short list of **only** the flagged items. The value is in what it
leaves out — counsel's time is the scarce thing, and a pack that
restates the whole draft wastes it.

## Where the money leaks

Work through these every turn. They are the routes by which a payable
earn-out becomes an unpayable one.

**Metric and calculation**
- Is the metric defined precisely, with worked examples attached?
- Are accounting policies locked to pre-closing practice, consistently
  applied? An unlocked policy is the quietest way to move the number.
- Can the buyer charge corporate overhead, management fees, integration
  costs or transfer pricing to the business?
- How are acquisitions, divestitures or new product lines during the
  period treated?
- Is there catch-up or carry-forward if one year misses and the next
  beats target?

**Buyer conduct after closing**
- Is there an express covenant to run the business consistent with past
  practice, or at least not to act with the purpose of reducing the
  earn-out? Most deals have no such covenant; that is exactly why the
  literal reading hurts.
- Specific restrictions needing seller consent: budget, headcount,
  pricing, moving customers, merging the business into other entities.
- Is the business kept separately trackable, so the metric can actually
  be measured?
- Is working capital and investment committed?

**Acceleration (full payout)**
- On sale of the business or change of control of the buyer?
- On buyer breach of the earn-out covenants?
- On the seller's termination without cause, or resignation for good
  reason?

**Set-off and security**
- Can the buyer withhold payment against indemnity claims — and if so,
  only finally determined ones, or disputed ones too? "Disputed" turns
  the earn-out into an option.
- Is there escrow, a guarantee or other security?

**Lender restrictions (specific to a PE buyer)**
- Will the buyer's credit agreement subordinate or block earn-out
  payments when covenants are tight? Ask to see the relevant debt terms
  and any intercreditor or subordination arrangements. This one is
  routinely missed because the debt documents are not in the data room.

**Information and disputes**
- Reporting, books-and-records and audit rights during the period?
- A clear dispute process — an independent accountant as expert on
  calculation only, with legal questions reserved?
- Timelines for delivering statements, objecting, and paying?

**Employment**
- Is the earn-out tied to continued employment? That creates forfeiture
  risk and can change the tax treatment. Flag it for the tax adviser
  rather than reasoning about the tax here.

## Rules for every output

- **Cite the clause for every finding.** Quote it; do not paraphrase a
  clause and then grade the paraphrase.
- **Distinguish what the draft says from what it omits.** An absent
  protection is the most common finding and the easiest to overlook,
  because there is no text to react to. Check the list above for
  silence, not just for bad wording.
- **Never draft communications to the buyer** without being told to.
- **Nothing here is legal or tax advice.** Senior M&A counsel and the
  Australian tax adviser make every call. This produces their inputs.
- Say what you could not check and why. A review that reports only what
  it found, and not what it could not reach, reads as more complete than
  it is.
