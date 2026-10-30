"""Point-in-time lookup over the Australian legislative instruments corpus.

A deal asks a question ordinary legal search answers badly: not "what
does this say?" but "what did this say on the day we signed, and who
has changed it since?". The corpus is a git history in which every
commit is one amending instrument taking effect, so both questions are
a git command. This server makes them tools.

Nothing here reaches the network. It reads a local clone of
https://github.com/drfinlaymccall/australia-instruments, whose path
comes from AU_INSTRUMENTS_CORPUS.

Speaks newline-delimited JSON-RPC over stdio.
"""

import json
import os
import re
import subprocess
import sys

CORPUS = os.environ.get("AU_INSTRUMENTS_CORPUS", "")
PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
SERVER = {"name": "au-instruments", "version": "0.1.0"}
INSTRUCTIONS = (
    "Australian Commonwealth legislative instruments as a point-in-time "
    "record: foreign investment screening, merger notification and "
    "takeovers. Every answer is the text in force on the date asked for, "
    "with the instrument that last changed it. This is source material "
    "for advice, not advice."
)
MAX_CHARS = 40_000


class Problem(Exception):
    pass


def git(*args, check=True):
    if not CORPUS or not os.path.isdir(os.path.join(CORPUS, ".git")):
        raise Problem(
            "No corpus. Set AU_INSTRUMENTS_CORPUS to a clone of "
            "australia-instruments; it is currently %r."
            % (CORPUS or "unset"))
    done = subprocess.run(["git", "-C", CORPUS] + list(args),
                          capture_output=True, text=True, timeout=60)
    if check and done.returncode != 0:
        raise Problem("git %s failed: %s" % (" ".join(args), done.stderr.strip()))
    return done.stdout


def instruments():
    """Folder name -> instrument title, from the corpus itself."""
    out = {}
    for line in git("ls-tree", "--name-only", "HEAD", "corpus/").splitlines():
        folder = line.rstrip("/").split("/")[-1]
        if not folder:
            continue
        intro = git("show", "HEAD:corpus/%s/intro.md" % folder, check=False)
        title = intro.splitlines()[0].lstrip("# ").strip() if intro else folder
        out[folder] = title
    return out


def resolve_instrument(name):
    """Match a folder, a register id or part of a title to one instrument."""
    known = instruments()
    if name in known:
        return name
    wanted = re.sub(r"[^a-z0-9]+", "", (name or "").lower())
    if not wanted:
        raise Problem("Name an instrument. Known: %s" % ", ".join(sorted(known)))
    hits = [f for f, title in known.items()
            if wanted in re.sub(r"[^a-z0-9]+", "", f + title.lower())]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise Problem("No instrument matches %r. Known: %s"
                      % (name, ", ".join(sorted(known))))
    raise Problem("%r matches more than one: %s" % (name, ", ".join(sorted(hits))))


def tag_on(folder, date):
    """The compilation in force on a date: the latest tag at or before it."""
    tags = sorted(t for t in git("tag", "-l", "%s/*" % folder).split()
                  if t.rsplit("/", 1)[1] <= date)
    if not tags:
        first = sorted(git("tag", "-l", "%s/*" % folder).split())
        raise Problem(
            "The record for %s starts %s; nothing was recorded on %s."
            % (folder, first[0].rsplit("/", 1)[1] if first else "(never)", date))
    return tags[-1]


def provision_path(folder, provision):
    """Accept '52', 's 52', 'section 52', '6.10.01', 'reg 6.10.01', '1-9'."""
    raw = (provision or "").strip()
    number = re.sub(r"^(?:sections?|ss?\.?|regulations?|regs?\.?|r\.?|clause|cl\.?)\s*",
                    "", raw, flags=re.I).strip()
    if not number:
        raise Problem("Name a provision, such as '52' or '6.10.01'.")
    if "." in number:
        return "r-%s.md" % number
    if "-" in number:
        return "s-%s.md" % number
    match = re.match(r"^(\d+)(.*)$", number)
    return "s-%s.md" % (match.group(1).zfill(3) + match.group(2) if match else number)


def last_change(folder, path, tag):
    """The commit that last touched a provision at or before a tag."""
    out = git("log", "-1", "--format=%H%n%an%n%ad%n%B", "--date=short",
              tag, "--", "corpus/%s/%s" % (folder, path), check=False)
    if not out.strip():
        return None
    sha, author, date, body = (out.split("\n", 3) + ["", "", "", ""])[:4]
    trailers = dict(re.findall(r"^([A-Za-z-]+): (.*)$", body, re.M))
    return {"commit": sha[:12], "amending_instrument": author, "in_force": date,
            "compilation": trailers.get("Compilation"),
            "compilation_id": trailers.get("Compilation-id"),
            "kind": trailers.get("Kind")}


# --- tools ---------------------------------------------------------------

def t_provision_on_date(args):
    folder = resolve_instrument(args.get("instrument", ""))
    date = date_arg(args.get("date"))
    path = provision_path(folder, args.get("provision", ""))
    tag = tag_on(folder, date)
    text = git("show", "%s:corpus/%s/%s" % (tag, folder, path), check=False)
    if not text.strip():
        raise Problem(
            "%s has no %s in the compilation in force on %s (%s). Use "
            "instrument_on_date to list what it did have."
            % (folder, path, date, tag.rsplit("/", 1)[1]))
    return {"instrument": folder, "provision": path, "date": date,
            "compilation_in_force_from": tag.rsplit("/", 1)[1],
            "last_changed_by": last_change(folder, path, tag),
            "text": text[:MAX_CHARS]}


def t_instrument_on_date(args):
    folder = resolve_instrument(args.get("instrument", ""))
    date = date_arg(args.get("date"))
    tag = tag_on(folder, date)
    names = [n.split("/", 2)[2] for n in
             git("ls-tree", "-r", "--name-only", tag, "corpus/%s/" % folder).splitlines()
             if n.endswith(".md")]
    headings = {}
    for name in names:
        if name == "intro.md":
            continue
        blob = git("show", "%s:corpus/%s/%s" % (tag, folder, name), check=False)
        line = next((l for l in blob.splitlines() if l.startswith("# ")), "")
        headings[name] = line[2:].strip()
    return {"instrument": folder, "date": date,
            "compilation_in_force_from": tag.rsplit("/", 1)[1],
            "provisions": headings, "count": len(headings)}


def t_what_changed(args):
    folder = resolve_instrument(args.get("instrument", ""))
    since, until = date_arg(args.get("since")), date_arg(args.get("until"))
    if since > until:
        raise Problem("'since' is after 'until'.")
    scope = ["--", "corpus/%s/" % folder]
    if args.get("provision"):
        scope = ["--", "corpus/%s/%s" % (folder, provision_path(folder, args["provision"]))]
    out = git("log", "--reverse", "--format=%x00%H%n%an%n%ad%n%B", "--date=short",
              "--since=%s" % since, "--until=%s 23:59" % until, *scope)
    changes = []
    for block in out.split("\x00"):
        if not block.strip():
            continue
        sha, author, date, body = (block.split("\n", 3) + ["", "", "", ""])[:4]
        trailers = re.findall(r"^Affecting: (.*)$", body, re.M)
        kind = re.search(r"^Kind: (.*)$", body, re.M)
        changes.append({"commit": sha[:12], "amending_instrument": author.strip(),
                        "in_force": date.strip(),
                        "kind": kind.group(1) if kind else None,
                        "provisions_affected": trailers})
    return {"instrument": folder, "since": since, "until": until,
            "changes": changes, "count": len(changes)}


def t_find_in_law(args):
    query = (args.get("query") or "").strip()
    if len(query) < 3:
        raise Problem("Give at least three characters to search for.")
    date = date_arg(args.get("date"))
    folders = ([resolve_instrument(args["instrument"])] if args.get("instrument")
               else sorted(instruments()))
    hits = []
    for folder in folders:
        try:
            tag = tag_on(folder, date)
        except Problem:
            continue
        out = git("grep", "-n", "-i", "-F", "-e", query, tag,
                  "--", "corpus/%s/" % folder, check=False)
        for line in out.splitlines()[:40]:
            _ref, _, rest = line.partition(":corpus/%s/" % folder)
            name, _, body = rest.partition(":")
            hits.append({"instrument": folder, "provision": name,
                         "line": body.partition(":")[2].strip()[:300]})
    return {"query": query, "date": date, "hits": hits[:60], "count": len(hits)}


def date_arg(value):
    text = (value or "").strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise Problem("Give a date as YYYY-MM-DD (the day the question is "
                      "about, such as the day a deal signed).")
    return text


TOOLS = [
    ("provision_on_date", t_provision_on_date,
     "The text of one provision as it stood on a date, with the instrument "
     "that last changed it. Use this instead of quoting a provision from "
     "memory: the wording of a threshold or an exemption is often what the "
     "question turns on, and it changes.",
     {"instrument": "Instrument: a folder name, a register id, or part of "
                    "the title (e.g. 'foreign acquisitions').",
      "provision": "Provision number: '52', 'section 52', '6.10.01', "
                   "'reg 6.10.01', '1-9'.",
      "date": "YYYY-MM-DD. The day the question is about."},
     ["instrument", "provision", "date"]),
    ("instrument_on_date", t_instrument_on_date,
     "Every provision an instrument had on a date, with its heading. Use it "
     "to see what existed then, before asking for any one provision.",
     {"instrument": "Instrument name, register id, or part of the title.",
      "date": "YYYY-MM-DD."},
     ["instrument", "date"]),
    ("what_changed", t_what_changed,
     "Every amendment to an instrument between two dates, each with the "
     "amending instrument that made it and the provisions it touched. Use "
     "it to answer 'what has moved since we signed?'.",
     {"instrument": "Instrument name, register id, or part of the title.",
      "since": "YYYY-MM-DD, inclusive.",
      "until": "YYYY-MM-DD, inclusive.",
      "provision": "Optional: narrow to one provision."},
     ["instrument", "since", "until"]),
    ("find_in_law", t_find_in_law,
     "Find a phrase in the instruments as they stood on a date. Returns the "
     "provisions it appears in, so they can then be read in full.",
     {"query": "A literal phrase, such as 'foreign government investor'.",
      "date": "YYYY-MM-DD.",
      "instrument": "Optional: one instrument instead of all."},
     ["query", "date"]),
]


def tool_list():
    out = []
    for name, _fn, description, properties, required in TOOLS:
        out.append({
            "name": name, "description": description,
            "inputSchema": {
                "type": "object", "additionalProperties": False,
                "properties": {k: {"type": "string", "description": v}
                               for k, v in properties.items()},
                "required": required}})
    return out


def handle(message):
    mid = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}
    if method == "initialize":
        asked = params.get("protocolVersion")
        return ok(mid, {
            "protocolVersion": asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
            "capabilities": {"tools": {}}, "serverInfo": SERVER,
            "instructions": INSTRUCTIONS})
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "tools/list":
        return ok(mid, {"tools": tool_list()})
    if method == "tools/call":
        name = params.get("name")
        entry = next((t for t in TOOLS if t[0] == name), None)
        if entry is None:
            return ok(mid, {"content": [{"type": "text",
                                         "text": "No tool named %r." % name}],
                            "isError": True})
        try:
            result = entry[1](params.get("arguments") or {})
        except Problem as problem:
            return ok(mid, {"content": [{"type": "text", "text": str(problem)}],
                            "isError": True})
        except Exception as error:                       # noqa: BLE001
            return ok(mid, {"content": [{"type": "text",
                                         "text": "%s: %s" % (type(error).__name__, error)}],
                            "isError": True})
        text = json.dumps(result, indent=1, ensure_ascii=False)
        return ok(mid, {"content": [{"type": "text", "text": text[:MAX_CHARS]}],
                        "structuredContent": result})
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": "Method not found: %s" % method}}


def ok(mid, result):
    return None if mid is None else {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    for raw in sys.stdin:
        if not raw.strip():
            continue
        try:
            message = json.loads(raw)
        except ValueError:
            reply = {"jsonrpc": "2.0", "id": None,
                     "error": {"code": -32700, "message": "Parse error"}}
        else:
            reply = handle(message)
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
