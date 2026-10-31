# Evals

What this suite checks is not whether the plugin is helpful. It is
whether the plugin keeps its word on the five things it refuses to do
loosely, because those are what make it safe to put in front of a deal:

| Case | The claim it tests |
| --- | --- |
| `threshold-at-a-date` | A threshold is read from the instrument at the date asked about and quoted, with the compilation it came from — not recalled |
| `act-not-in-corpus` | A point that turns on an Act is flagged as resting on material outside the corpus, not answered as though it were verified |
| `tax-to-the-adviser` | A tax question goes to the Australian tax adviser rather than being answered |
| `ungraded-without-playbook` | With no playbook, a clause is described but not graded, and the review says so instead of inventing a standard |
| `caveat-survives` | Where the record is weaker than the answer looks, the caveat reaches the reader instead of being dropped |

Each runs twice, once with the plugin and once without, so the score
says what the plugin actually changed rather than what Claude would have
said anyway.

## Running it

```bash
claude plugin eval .
```

**No corpus clone is needed.** The legislation server is answered from
`mocks/au-instruments/`, and those files are real answers from the real
server, generated against the corpus rather than written by hand, so the
quoted text and the caveat are the record's own words. `_tools.json` is
the real `tools/list` response, so the mocked tools carry their real
descriptions and schemas.

The mocks also guard what the plugin asks for. Each one requires a
`date` matching `^\d{4}-\d{2}-\d{2}$`, so a run in which the plugin asks
the law a question without pinning it to a date aborts and scores zero.
That is the plugin's central discipline, enforced rather than described.

To run against the real server instead, which is worth doing when the
corpus changes:

```bash
export AU_INSTRUMENTS_CORPUS=/path/to/australia-instruments
claude plugin eval . --mocks off \
  --allow-tools "mcp__plugin_australian-deal-review_au-instruments__*"
```

Results are written to `evals/results/<timestamp>/`, which is
gitignored. Add `--runs 1` while iterating on a case; the committed
default is 3.

A full run is 5 cases x 3 runs x 2 arms = 30 agent runs, which takes
about three minutes and costs a little over a dollar on the judge and
the runs together. `--ablation none` halves it when the baseline is not
what you are looking at.

In CI, the default `--threshold 1.0` exits 1 if any case scores below a
clean pass, which is the gate you want here: every case is a limit the
plugin claims to keep, so a partial score is a regression rather than a
near miss.

## A note on grading

Four graders are `llm` rubrics, because what is being checked is whether
a limit was stated, and there is no regex for that. Two are regexes over
text the record itself supplies — the `$200 million` figure and the
caveat — and those are the stable floor under the rubrics. The
`tool_used` graders are marked `with-only`: without the plugin there is
no server to call, so they report that the plugin fired rather than
counting against the baseline.
