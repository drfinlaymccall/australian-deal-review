---
name: australian-deal-law
description: The Australian-side checks on a cross-border acquisition - foreign investment screening (FIRB), merger notification (ACCC), takeovers relief, and the tax and restraint questions that sit outside this corpus. Use when reviewing a transaction document with an Australian target or seller, when asked whether a deal needs FIRB or ACCC clearance, when a draft changes anything about approvals, conditions, longstop dates or restraints, and whenever a threshold figure or an exemption is about to be stated. Also use when asked what the law said on a particular date.
version: 0.2.0
---

# Australian-side checks

A US buyer's counsel runs the US side. The Australian side is where
things get missed, because it is a different regulator, a different
statute and, since 1 January 2026, a different regime from the one most
precedent documents were drafted against.

## The rule that matters most

**Never state a threshold, an exemption or a test from memory.** Read it
with `provision_on_date`, at the date the question is about, and quote
it. These figures move: the monetary thresholds are indexed, the merger
regime is new, and the foreign investment regulation has been amended
twenty times since 2015.

The date to ask about is usually one of:

- the date of the draft under review (what the clause is being written against);
- the signing date (what the condition precedent will be tested against);
- the expected completion date (what will actually apply);
- today (what has changed since the last turn).

When those give different answers, that difference **is** the finding.

## What this corpus holds, and what it does not

`au-instruments` holds the **instruments** — regulations and
determinations — not the Acts they are made under.

| In the corpus | Not in the corpus |
| --- | --- |
| Foreign Acquisitions and Takeovers Regulation 2015 | Foreign Acquisitions and Takeovers Act 1975 |
| Competition and Consumer (Notification of Acquisitions) Determination 2025 | Competition and Consumer Act 2010 |
| Competition and Consumer (Notification of Acquisitions—Forms) Determination 2025 | Corporations Act 2001 |
| ASIC Corporations (Takeover Bids) Instrument 2023/683 | Income Tax Assessment Act 1997 |
| Corporations Regulations 2001 | |

This matters and must be said out loud in any output. **The instruments
carry the thresholds and the exemptions; the Acts carry the operative
rule.** A threshold read here tells you what number applies, not whether
the obligation bites. Anything resting on an Act is for counsel, and
must be flagged as unverified here rather than asserted.

### Provisions, and the forms that are not provisions

Most law in the corpus is one file per section (`s-1-9.md`) or per
regulation (`r-6.10.01.md`). The prescribed **forms** are not: in the
Forms Determination the notification forms are whole Divisions with no
section headings under them, so they are filed by the Part and Division
that hold them — `part-6/div-2.md` is the short-form notification,
`div-3` the long form, `div-4` the public benefit application. Ask for
them by that name:

    provision_on_date(
      instrument="competition-and-consumer-notification-of-acquisitions-forms-determination-2025",
      provision="part-6/div-2", date="<the date>")

The form is what the ACCC actually requires to be filled in, so it is
the fastest way to see what a notification will cost the seller in
disclosure. Read it before advising on timetable: the information it
demands of each party is the real work in a notification, not the fee.

### Dates the record does not cover

Every answer names the compilation it was read from
(`compilation_in_force_from`). Where the record is weaker than the
answer looks, the answer also carries a `caveats` list. **Say the
caveat in the output. Do not drop it**, and do not state a threshold
from a caveated answer without it.

Two things cause one. The register publishes some older compilations
only as legacy `.doc` or `.rtf` files, and those are not in the
corpus; for the Corporations Regulations they are scattered through
its first decade rather than sitting in a block at the start, so a
date in that range can resolve to a committed day that misses an
amendment entirely. Each instrument's `no_gaps_from` in `corpus.json`
is the day its record becomes continuous. And separately, a date
between two compilations resolves to the earlier one — correct, but
worth saying when the two are months apart.

For anything load-bearing on a date before `no_gaps_from`, read the
register itself. Do not assert it from here.

Nothing about **tax** is in this corpus. The look-through CGT treatment
of an earn-out right sits in Subdivision 118-I of the Income Tax
Assessment Act 1997, which is not here. Treat every tax point as a
question for the Australian tax adviser, never as a finding.

**Do not lead with the answer and caveat it afterwards.** "Probably
yes, subject to confirmation" is a finding with a disclaimer stapled to
it, and the disclaimer is the half that falls off when the sentence is
repeated to someone else. Say first that it is the adviser's question.
Then set out what it turns on, and what the adviser would need to know
to settle it. That ordering is the whole protection: it is what stops
an unverified recollection being carried into a negotiation as advice.

## Foreign investment screening (FIRB)

The Foreign Acquisitions and Takeovers Regulation 2015 prescribes the
monetary thresholds, what counts as a foreign government investor, the
land categories and the exemptions.

The point that catches PE buyers: a fund with sovereign or government
pension money upstream can be a **foreign government investor**, for
which the monetary threshold is nil, so approval is needed whatever the
deal size. Read the definition at the relevant date
(`provision_on_date`, "meaning of foreign government investor") and
check it against what the buyer has actually disclosed about its
investors. If the buyer has not disclosed that, **the gap is the
finding** — not an assumption either way.

Then check, as questions for counsel:

- Who carries the risk of a delay or a condition — buyer or seller?
- Is the longstop date long enough for the actual decision period?
- Could a condition imposed on approval restrict how the business is run
  during the earn-out period? If so, the earn-out targets were set
  against a business that will not be run that way.

## Merger notification (ACCC)

The Competition and Consumer (Notification of Acquisitions)
Determination 2025 sets the money tests. Under the regime in force from
1 January 2026, an acquisition connected with Australia that meets them
must be notified and cleared **before** completion unless exempt.

Read the tests rather than recalling them. In the determination as made
they are grouped as: a combined acquirer/target revenue test, acquired
shares or assets revenue tests, an accumulated version of those, a
transaction value test, and a very large corporate group test. Use
`instrument_on_date` to list the provisions at the date in question, then
`provision_on_date` on each test that could be met, and quote the figure.

Watch the **accumulated** tests in particular. They pick up earlier
acquisitions, so a deal under the headline threshold can still be
notifiable because of what the buyer or the target bought before. Ask
what has been acquired in the look-back period; if nobody knows, say so.

Check too:

- Is notification a condition precedent, and who files?
- What happens to the earn-out clock while clearance is pending?
- Can the ACCC's own conditions change how the business is run during
  the earn-out period?

## Takeovers

The ASIC Corporations (Takeover Bids) Instrument 2023/683 gives relief
from parts of the Corporations Act takeover rules. It is relevant where
the target is a listed or widely-held company rather than a private
sale. Where the deal is a private share sale it usually is not engaged —
but say that it was considered and why it does not apply, rather than
leaving it unmentioned.

## Restraints

A restraint given on a sale of business is treated differently from an
employee non-compete. Two live questions for counsel:

- Does the restraint still bind the seller if the buyer stops paying the
  earn-out? A restraint that survives non-payment is a one-way deal.
- Is its scope and duration reasonable enough to be enforced, and has
  the competition-law position on sale-of-business restraints been
  checked under the current merger reforms?

## What has changed since we last looked

At the start of every review turn, run `what_changed` on each instrument
from the date of the previous turn to today. A change to a threshold or
an exemption between turns can move a deal from not-notifiable to
notifiable without a word of the draft changing, and nobody will
otherwise notice.

## How to report a finding

Every finding carries:

1. the clause of the draft it is about, quoted;
2. the provision it turns on, quoted, with the date it was read at and
   the instrument that last changed it (`provision_on_date` returns all
   three);
3. whether it rests on anything **not** in this corpus — an Act, tax law,
   a fact about the buyer nobody has supplied;
4. the question for counsel, phrased so it can be answered yes or no.

A finding that cannot carry point 2 is an assumption. Label it as one.
