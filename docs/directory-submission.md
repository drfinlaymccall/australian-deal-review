# Submitting this plugin to Anthropic's directory

Prepared 31 October 2026. Everything here stops short of the submission
itself, which needs a signed-in developer portal session.

Sources, all read 31 October 2026: the submission guide, the
[pre-submission checklist][check], the [publishing overview][publish],
[plugin feature support across platforms][surfaces], the
[Software Directory Policy][policy] (last updated 24 October 2026, a
week before this was written — re-read it before submitting) and the
[Software Directory Terms][terms]. The AUP's High-risk Use Case
Requirements are quoted where they bite.

[check]: https://claude.com/docs/plugins/pre-submission-checklist
[publish]: https://claude.com/docs/directory/publish
[surfaces]: https://claude.com/docs/plugins/platform-support
[policy]: https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy
[terms]: https://support.claude.com/en/articles/13145338-anthropic-software-directory-terms

## Where it stands

**Nothing blocks submission.** `claude plugin validate .` is clean,
including `--strict`. One finding is close to certain at review, and it
is a hold rather than a rejection: the plugin starts an MCP server that
is not a file inside the plugin. The case for leaving that alone is
below, with what it costs.

| | |
| --- | --- |
| Hard blockers | None found |
| Expected reviewer hold | `MCP server command wasn't read` — the server lives outside the plugin |
| Behaviour tested | `evals/`, five cases: 1.00 with the plugin against 0.28 without |
| Needs Finlay | A paid Claude plan, a connected GitHub account, and the portal itself |

## The listing copy

### Short description

The directory reads the short description from `plugin.json`. The
current one already carries the limit in its last sentence, so it should
go in unchanged rather than be tightened into something that reads
better and claims more:

> Review deal documents turn by turn against a counsel-approved
> playbook, with the Australian-side checks -- foreign investment
> screening, merger notification, takeovers -- read from the legislation
> as it stood on the date that matters. Goes deepest on the earn-out.
> Preparation for counsel, not advice.

### Long description

**The directory uses the README as the listing's description.** There is
no separate field to write, so the README is the listing copy. It has
been left saying what it said, and the `Setup` section now spells out
that the MCP server is one you run yourself.

If the portal does offer a free-text field, this is the paragraph to put
in it:

> An earn-out is the part of a sale price most likely to be argued about
> afterwards, and the protection is whatever the contract says
> expressly. This plugin runs the same review on every new draft: what
> changed since the last turn, each earn-out clause graded against
> counsel's playbook, the Australian-side checks, an updated issues
> register, and a counsel pack holding only the flagged items. The
> Australian checks — foreign investment screening, merger notification,
> takeovers, restraints — are read out of the legislative instruments
> themselves at the date that matters and quoted, not recalled, because
> the thresholds are indexed, the merger regime is new since 1 January
> 2026, and an answer that is right for today may be wrong for
> completion. That difference between dates is treated as the finding.

### Category

`category` is not a `plugin.json` field. The marketplace entry already
carries `"category": "legal"`, which is what `/plugin install` reads.
Where the listing is placed in the directory is Anthropic's decision at
review; there is nothing to apply for. **Legal** is the intended
category, with M&A and contract review as the use case.

### The limits paragraph

This is the part not to trim. It is also, as the policy check below
shows, the part that makes the plugin admissible at all:

> **What this does not do.** It is preparation for counsel, not legal or
> tax advice: senior M&A counsel and the Australian tax adviser make
> every call, and this produces their inputs. The corpus behind it holds
> Commonwealth legislative *instruments* — the regulations and
> determinations carrying the thresholds and exemptions — and not the
> Acts they are made under, so a threshold read here tells you what
> number applies, not whether the obligation bites. Anything resting on
> an Act is flagged as unverified rather than asserted. There is no tax
> legislation in it at all, so every tax question goes to the adviser
> rather than being answered. Until counsel fills in the playbook,
> reviews describe clauses without grading them, and say so. The corpus
> covers five instruments, and each one's record becomes continuous only
> from a stated date; before that date an answer carries a caveat naming
> the gap and says to read the Register itself.

### Three worked examples

Policy 3.E asks for at least three. These are reviewable as they stand,
and the first two need only the corpus, not a deal:

1. *"What was the combined acquirer/target revenue test for merger
   notification on 1 January 2026, and which instrument set that
   figure?"* — reads the Notification of Acquisitions Determination 2025
   at a date and quotes the provision with the compilation it came from.
2. *"What has changed in the Foreign Acquisitions and Takeovers
   Regulation 2015 since 1 July 2023?"* — walks the amending instruments
   between two dates.
3. `/deal-setup`, then `/australia-check` on a share acquisition signing
   1 March 2026 and completing 1 July 2026 — runs foreign investment,
   merger notification, takeovers and restraints at each of the deal's
   dates and reports where the answers differ.

## The policy check, point by point

### Validation and the automated scan

Checked against the pre-submission checklist. Everything below was run
or read, not assumed.

| Check | This plugin |
| --- | --- |
| Folder holds `.claude-plugin/plugin.json` | Yes, at the repository root |
| One plugin per submission | One. See the marketplace note below |
| No symlinks, submodules, LFS pointers | None |
| No `.DS_Store` / `Thumbs.db` / `__MACOSX` | None |
| Cross-platform file names | All lowercase, hyphens and dots only |
| Repo under 50 MiB archived, under 10,000 files | 81 KiB, 17 files |
| `name` lowercase, hyphenated, not reserved | `australian-deal-review` |
| `description`, `author`, `version` set | Yes; `version` is `0.2.0` |
| README of 40+ words in the plugin folder | Yes |
| `LICENSE` present or `license` set | Both — Apache-2.0 |
| Every file under 256 KiB, 512 files or fewer | Largest is this document at 20 KiB; the icon is 16 KiB |
| Only text files and complete images | Markdown, JSON, one PNG |
| MCP server declared with `command` and `args` | Yes, not a `.mcpb` bundle |
| `.mcp.json` parses and matches the schema | Yes — verified, see below |
| No package launchers (`npx`, `uvx`, `pipx`) | None. `python3` with a plain path |
| No credentials anywhere, examples included | None. No API keys exist in this design |
| No credential read from the user's environment | `AU_INSTRUMENTS_CORPUS` is a filesystem path, not a secret |
| Valid YAML front matter on every component | Four commands, two skills; all six parse, every `description` a string |
| `icon` present | Added: `.claude-plugin/icon.png`, 1024×1024 |

Two things worth recording because they were checked rather than
believed:

- **The `.mcp.json` really is read.** It is a bare server map with no
  `mcpServers` wrapper. Introducing a deliberate error into it in a
  scratch copy produced `au-instruments.args[1]: references
  ${user_config.…}`, so the validator parses the entry and reports on
  it. The file is not being silently skipped, and the wrapped form
  behaves identically.
- **The folder is both a plugin and a marketplace.** The validator says
  so: *"The plugin directory treats such a folder as a plugin, so these
  checks cover only the plugin in this folder."* The checklist blocks
  with **Pick one plugin first** where a marketplace holds several
  plugins. This marketplace holds exactly one, whose source is the root
  — the same folder being submitted — so it should pass. If that finding
  does fire, submit with the plugin path left empty; the marketplace
  manifest is there for `/plugin install` and is not what the directory
  reads.

### The security scan

The scan looks for undisclosed behaviour: data sent elsewhere, hidden
code, changes to Claude's permissions. This plugin is unusually easy to
clear, and the reasons are worth stating in the submission.

- Nothing is compiled, packed or minified. Every file is Markdown or
  JSON a reviewer can read end to end.
- The plugin makes no network calls at all. Neither does the server it
  starts: it shells out to `git` against a local clone.
- The only thing that leaves the plugin is the path in
  `AU_INSTRUMENTS_CORPUS`, which the user sets themselves.
- There are no hooks, no `bin/`, no settings changes, no agents.

### Policy 1 — safety, and the legal high-risk rules

**This is the section that matters, and the plugin is already on the
right side of it.** Policy 1.A puts legal among the high-risk areas and
requires compliance with the AUP's High-risk Use Case Requirements. 1.B
then says that software *providing* a high-risk use case must have
human-in-the-loop measures and direct disclosure to consumers **to be
included in the directory**.

The AUP defines the legal high-risk area as advising someone on their
legal rights, obligations or liability, or preparing legal documents for
them to sign or file. It requires a qualified person who meaningfully
reviews the output and has authority to change it, who remains
responsible for what is delivered, and disclosure that AI was used. It
excludes *"general information or educational content, including
explaining what a law says"* unless applied to someone's circumstances.

Applied here:

- The four corpus tools on their own sit inside that exclusion. Quoting
  what an instrument said on a date is explaining what a law says.
- The review workflow does not: it is applied to a particular party's
  draft, so it falls inside the high-risk area, and the measures apply.
- The plugin already meets them, by construction rather than by
  disclaimer. Counsel is the qualified reviewer with authority to
  change; `earnout-review` requires that "senior M&A counsel and the
  Australian tax adviser make every call"; grading stops entirely until
  counsel supplies the playbook; and every finding must say what it
  could not check.

**The consequence for the listing copy: the limits are a condition of
admission, not a disclaimer.** Trimming "preparation for counsel, not
advice", or the statement that the Acts and tax law are out of the
corpus, would not just overclaim — it would weaken the thing the policy
requires. The one gap to close is the disclosure leg: where a counsel
pack produced here is passed to a client, counsel has to tell them AI
was used. That is a line for counsel's own engagement terms, not a code
change.

Other parts of Policy 1: the plugin collects nothing from the user's
context, stores nothing, builds no profile, and reads none of Claude's
memory or history (1.D–1.G). Deal documents stay in the user's own
working folder and are never part of the plugin.

### Policy 2 — compatibility of the instructions

The two skills and four commands are plain Markdown with nothing hidden,
encoded or obfuscated (2.G). The server's four tools are narrowly
described and named for what they do (2.A, 2.B). Nothing instructs
Claude to pull behaviour from an external source (2.F) — the plugin's
whole point is that the only external thing it reads is a local git
clone the user chose.

### Policy 3 — developer requirements

| Requirement | Position |
| --- | --- |
| 3.A Privacy policy | Not required. It applies to software that collects user data or connects to a remote service; this does neither. Say so plainly at the Data handling step |
| 3.B Contact and support channel | `supportUrl` now points at the repository's issues |
| 3.C Document how it works and how to troubleshoot | README, now including the server setup and its failure mode |
| 3.D Testing account with sample data | No account exists. The nearest equivalent now ships: `evals/mocks/` holds real recorded answers, so a reviewer runs `claude plugin eval .` and sees the behaviour without the corpus at all. The three commands below still give the fuller check |
| 3.E Three working examples | Three drafted above, plus five runnable cases in `evals/` |
| 3.F Own or control what it connects to | It connects to nothing. The corpus repository is Finlay's |
| 3.G, 3.H Maintain it, report material changes | Ongoing |

### Policy 4 — unsupported use cases

None apply. No money movement, no image, audio or video generation, no
advertising, no adult content.

### Policy 5 — MCP server requirements

These bind the corpus's server, which was checked rather than assumed:

| | |
| --- | --- |
| 5.A Graceful errors | Verified. With the variable pointing nowhere it answers `isError: true` and *"No corpus. Set AU_INSTRUMENTS_CORPUS to a clone of australia-instruments; it is currently '…'"*, naming the bad value |
| 5.C Tool names under 64 characters | Longest is `instrument_on_date`, 18 |
| 5.E Annotations, in particular `readOnlyHint`, `destructiveHint`, `title` | Present: `title`, `readOnlyHint: true`, `idempotentHint: true`, `openWorldHint: false`. `destructiveHint` is not applicable to a read-only tool |
| 5.G Reasonably current dependencies | None. Python 3.11+ standard library only |
| 5.D, 5.F Remote transport and OAuth | Not applicable. There is no remote server |

### Which surfaces it works on

Worth knowing before submitting, because the portal derives the
supported surfaces and shows them, and because the answer is not
"everywhere":

| Component | Chat | Cowork | Claude Code |
| --- | --- | --- | --- |
| Skills and commands | Loads | Loads | Loads |
| The legislation server | **Ignored** | Only when the session runs on the user's computer | Loads |

A local MCP server is ignored in claude.ai chat. The Australian checks
are the plugin's distinctive half and they need the server, so this is
realistically a Claude Code plugin. The README now says so in a table
rather than leaving someone to find out.

## Tested behaviour, not just structure

The checklist is explicit that validation and the scan check how a
plugin is built, not whether it helps: *"test the plugin's output and
how it loads on the surfaces your users will use."* `evals/` is that
test, and `evals/README.md` says how to run it.

Five cases, one for each limit this plugin is admissible because of,
each run with the plugin and again without it, five runs per arm:

| Case | With | Without | Delta |
| --- | --- | --- | --- |
| `act-not-in-corpus` | 1.00 | 0.00 | +1.00 |
| `tax-to-the-adviser` | 1.00 | 0.00 | +1.00 |
| `ungraded-without-playbook` | 1.00 | 0.40 | +0.60 |
| `caveat-survives` | 1.00 | 0.48 | +0.52 |
| `threshold-at-a-date` | 1.00 | 0.50 | +0.50 |

Overall 1.00, mean delta +0.72, across 50 runs and about six minutes.

**Two of those rows are worth putting in front of a reviewer**, because
they say what the plugin is actually for. On `threshold-at-a-date` the
no-plugin arm quoted the $200 million figure correctly in every run and
still scored 0.50, because it could not say which compilation or
instrument that figure came from. On `ungraded-without-playbook` the
no-plugin arm found the same leaks in the clause, five runs out of five,
and still scored 0.40, because it graded the clause as a red line on its
own authority. What the plugin adds is not the analysis. It is the
sourcing and the restraint, which is the same thing Policy 1.B asks of a
high-risk listing.

**The suite needs no corpus clone.** `evals/mocks/au-instruments/` holds
real answers generated from the real server, so `claude plugin eval .`
reproduces the behaviour without cloning 35 MB. Each mock also guards
its input: every one requires a `date` matching `^\d{4}-\d{2}-\d{2}$`,
so a run in which the plugin asks the law a question without pinning it
to a date aborts and scores zero. The discipline is enforced, not
described.

**What building the suite found.** The first full run scored 0.67 on
`tax-to-the-adviser`: one run in three opened with "Short answer:
probably yes" and caveated afterwards, which is precisely the failure
the skill exists to prevent. `australian-deal-law` now says not to lead
with an answer and caveat it after, and the plugin version is raised to
0.3.0.

The grader needed correcting too. It had been penalising correctly
framed answers for containing detail, and the rewritten rubric judges
ordering instead of volume. That this is sharper rather than merely
looser was measured, not assumed: on the same case the no-plugin arm
still fails five runs out of five, every one of them opening with "Yes"
or "Probably yes".

## The external server: keep it, and why

`.mcp.json` runs `python3 -I ${AU_INSTRUMENTS_CORPUS}/tools/mcp_server.py`
— a file in the user's clone of a *separate* repository, not in the
plugin. The directory has opinions about this. They were read closely
because the design is deliberate.

**What the rules actually say.** Three provisions bear on it:

1. *"People who install the plugin get only the plugin folder, so
   everything the plugin runs has to be inside it"*, and keep every file
   an MCP server command uses inside the plugin folder. The stated
   blocking trigger is narrower than the rule: **Blocks** for *a
   `plugin.json` path that points outside the plugin folder*. This path
   is in `.mcp.json`, not a `plugin.json` component path, so the
   automated block should not catch it — but the plugin is plainly
   outside the requirement as written.
2. *"Start each local MCP server by running a file in the plugin with
   plain arguments"* → **Held for a reviewer**, finding **MCP server
   command wasn't read**. This one does catch us, squarely. A hold is
   not a rejection: a person reads the version before it goes live.
3. *"In the command of a hook or an MCP server, write each path in full
   from `${CLAUDE_PLUGIN_ROOT}`, with no other variable"* → **Blocks
   when the plugin folder is a subfolder of the repository.** The plugin
   is at its repository root, so this does not block today.

**Point 3 is a tripwire, and it answers the question of whether the repo
layout can stay as it is.** It can — but only in this shape. Moving the
plugin into a subfolder of a larger repository would turn a hold into a
hard block, because `${AU_INSTRUMENTS_CORPUS}` is a variable other than
`${CLAUDE_PLUGIN_ROOT}`. **Keep this plugin at the root of its own
repository.**

**Bundling the corpus instead is worse, and measurably so.** The
alternative is to copy the corpus and its server into the plugin folder.
Measured against the directory's own limits, that trades one hold for
two:

- The corpus is **1,730 tracked files**. The plugin limit is **512**, and
  exceeding it is *Held for a reviewer*.
- Its `cache/index.json` is **398 KiB**. The non-image file limit is
  **256 KiB**, also a hold.

So bundling holds too, on two counts instead of one, every version — and
it costs the thing the design exists to protect. There would then be two
implementations of a reader of a legal record, and they drift silently;
that has already happened once in this project, with a duplicated copy
falling behind on tool titles and annotations. A corrected reader would
then reach users through a plugin release instead of a `git pull`.

**Verdict: do not change it.** Submit as it stands. If a reviewer asks,
the answer is two sentences: the corpus is 1,730 files and cannot live
inside a 512-file plugin, and there is deliberately one implementation
of the reader, living with the record it reads. Both are checkable.

**What it costs, stated plainly.** A reviewer cannot exercise the
Australian tools without the corpus, and Policy 3.D's testing account
has no analogue here. Give them this in the submission notes:

```bash
git clone https://github.com/drfinlaymccall/australia-instruments.git
export AU_INSTRUMENTS_CORPUS=$PWD/australia-instruments
# then: /deal-setup, or ask what the merger notification
# revenue test was on 1 January 2026
```

**Held in reserve, not applied.** If the reviewer does push back, the
smallest change that answers them without touching the architecture is
to replace the ambient environment variable with a `userConfig` option
of type `directory`, referenced as `${user_config.corpus_path}`. The
server still lives with the corpus; only the way the path arrives
changes. It was tested: the validator understands `${user_config.*}` in
a local server's `args`. It is not being applied now because it is not
free — Cowork ignores a server whose `user_config` reference has no
default, so it would make Cowork support worse than the environment
variable does, and the README setup would need rewriting around a
prompt. Worth doing if asked, not before.

## What Finlay has to do in the portal

None of this can be done from here.

1. **A paid plan.** Pro, Max, Team or Enterprise. Free accounts cannot
   submit. On Team or Enterprise it must be an Owner, or a member with
   the Directory permission.
2. **Connect GitHub to claude.ai** in the organisation the listing
   should belong to long term, with an account that can push to
   `drfinlaymccall/australian-deal-review`. A connection made in another
   Claude organisation does not carry over. The first organisation to
   submit a given repository folder owns the listing.
3. **Push the icon before opening the portal.** The validator is
   explicit that the file becomes the listing icon *only once* — the
   first time the plugin is saved or submitted — and that changing it
   later does not change the icon. It is committed; it needs to be on
   `main` before step 4.
4. **Submit** at claude.ai/directory/manage → **Submit new** → **Plugin
   bundle**. Repository `drfinlaymccall/australian-deal-review`; leave
   the plugin path empty, because the plugin is at the root; leave the
   branch empty to follow `main`. Then **Validate** — the portal runs
   more checks than the command does.
5. **Data handling.** The answers are: reads no personal data; stores
   nothing; sends data to no service, declared or otherwise, because it
   makes no network calls; no retention, because nothing is kept; not
   intended for under-18s.
6. **Compliance.** Check the contact address and accept the four
   acknowledgements, which bind the plugin to the Directory Terms and
   Policy.
7. **Review and submit.** Choose how new versions arrive — the GitHub
   push webhook is the default and needs repository admin access, which
   Finlay has. Auto-publish can stay off; the first version is published
   by an Anthropic reviewer either way.

A plugin is not submitted as an MCP connector. That path is for *remote*
servers, and there is no remote server here and none planned. Nothing
needs hosting.

Two housekeeping points for afterwards: raise `version` in
`plugin.json` on every release, because the directory picks up each
commit on `main`; and an organisation may create only 10 submissions in
any 24 hours, with drafts and withdrawals counting.

The eval suite stays a manual gate, not a CI job. A full run with the
ablation arm is about $2.86 and six minutes; `claude plugin eval .`
alone, at the committed default of three runs per case, is about $1.70.
Run it before raising `version`, not on every push. What should run
before every push to `main` is `claude plugin validate . --strict`,
which makes no model calls and costs nothing. That check matters more
once the push webhook is live, because from then on a push to `main` is
a release.
