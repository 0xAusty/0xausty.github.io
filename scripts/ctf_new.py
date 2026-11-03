#!/usr/bin/env python3
"""Create a challenge-page stub for the Huntress CTF 2026 section of the site.

Usage (run from anywhere; every path is resolved from this file's location, so
it behaves the same from PowerShell, cmd.exe, Git Bash or a POSIX shell):

    python scripts/ctf_new.py day06-pool-party                # field note stub   (depth = "note")
    python scripts/ctf_new.py day06-pool-party --depth full   # full write-up stub (depth = "full")
    python scripts/ctf_new.py --list                          # catalog keys that have no page yet

What it does:

  1. Loads data/huntress_ctf_2026.json (the event catalog) and finds the entry
     whose "key" matches the argument. A path or a ".md" suffix is tolerated, so
     content/huntress-ctf-2026/day06-pool-party.md means day06-pool-party.
  2. Reads the Hugo archetype archetypes/huntress-ctf-2026.md and fills title,
     date (the release date), catalog_key and depth from the catalog, plus the
     lane's default tags and skills when the archetype leaves them empty, then
     adds a comment with the entry's day, lane, gm_id and web_no (the web lane's
     own numbering). draft stays true. A top-level `kind` is rewritten to
     `params.kind`: Hugo reserves `kind`, and .Params.kind reads the same.
     When the catalog marks the challenge unsolved, solved_by becomes [] with
     a TODO comment instead of the archetype's default attribution.
  3. Writes content/huntress-ctf-2026/<key>.md. An existing page is never
     overwritten: delete it yourself first if you really want a fresh stub.

The archetype is a Go template that `hugo new` evaluates against the catalog.
This script has no template engine, so it keeps the archetype's static skeleton
instead: every `{{ ... }}` action is dropped, every `{{ if }}`/`{{ with }}`/
`{{ range }}` block counts as false (a bare `{{ else }}` branch is kept), the
`{{-`/`-}}` trim markers are honoured, `{{</* name */>}}` escapes become real
`{{< name >}}` shortcodes and `{{/* ... */}}` comments are removed. The keys the
archetype would have filled through Hugo are then filled here from the catalog.
If the archetype file is missing, a built-in template with the same front-matter
keys is used and a warning is printed.

Standard library only (Python 3.8+). Exit status: 0 success, 1 refused or key
not found, 2 usage or template problem.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "huntress_ctf_2026.json"
ARCHETYPE_FILE = ROOT / "archetypes" / "huntress-ctf-2026.md"
CONTENT_DIR = ROOT / "content" / "huntress-ctf-2026"
DEPTHS = ("note", "full")

# Used only when archetypes/huntress-ctf-2026.md is missing. Same keys as the archetype.
FALLBACK_ARCHETYPE = """+++
title = ""
date = 1970-01-01                 # the challenge's release date (filled from the catalog)
draft = true
params.kind = "challenge"         # Hugo reserves a top-level "kind"; params.kind still reads as .Params.kind
catalog_key = ""                  # MUST match a key in data/huntress_ctf_2026.json
depth = "note"                    # "full" (curated write-up) | "note" (short field note)
featured = false                  # true -> appears in the hub's "Start here"
description = "One line: the key insight or the skill this shows. Used in lists, search and social cards."
# Who got it, most important first: autopilot | agent | hand | homebase
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   hand      → "Solved by hand (Austin)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]
tools = ["python"]
tags = []
skills = []                       # groups it on /portfolio/
toc = true
+++

<!-- Field note (depth = "note"): a few paragraphs. What the challenge asked, what the
     file was, how it was solved, one takeaway. -->

<!-- Full write-up (depth = "full") uses these H2 headings, in this order:
## The challenge
## Reading the prompt
## What was in the files
## The solve
## Making it deterministic
## Timed modes
## Dead ends
## Takeaways
-->
"""

_GO_COMMENT = re.compile(r"\{\{-?\s*/\*.*?\*/\s*-?\}\}", re.S)
_ACTION = re.compile(r"\{\{(?![<%])(-?)\s*(.*?)\s*(-?)\}\}", re.S)  # a template action; {{< >}} / {{% %}} shortcodes are not
_BLOCK_OPENERS = ("if", "with", "range", "define", "block")
_KEY_LINE = re.compile(r"^(\s*)([A-Za-z0-9_.-]+)(\s*=\s*)")
_TABLE_LINE = re.compile(r"^\s*\[")  # a TOML [table] header: keys after it are no longer top-level

# Lane defaults for tags/skills: the same ones archetypes/huntress-ctf-2026.md gives
# `hugo new` (keep the two in sync). Used only when the archetype leaves the key empty.
LANE_TAGS = {
    "warmups": ["encoding"], "metadata": ["forensics"], "script": ["malware-analysis"],
    "binary": ["reverse-engineering"], "mobile": ["android"], "web": ["web-exploitation"],
}
LANE_SKILLS = {
    "warmups": ["Automation & Tooling"], "metadata": ["Digital Forensics"], "script": ["Malware Analysis"],
    "binary": ["Reverse Engineering"], "mobile": ["Reverse Engineering"], "web": ["Web Application Security"],
}


def warn(msg: str) -> None:
    print(f"ctf_new: {msg}", file=sys.stderr)


def die(msg: str, code: int = 2):
    warn(msg)
    sys.exit(code)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------- catalog

def load_catalog() -> list:
    try:
        with DATA_FILE.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die(f"catalog not found: {DATA_FILE}")
    except json.JSONDecodeError as exc:
        die(f"catalog is not valid JSON ({rel(DATA_FILE)}): {exc}")
    challenges = data.get("challenges") if isinstance(data, dict) else None
    if not isinstance(challenges, list) or not challenges:
        die(f'{rel(DATA_FILE)} has no "challenges" array')
    return challenges


def normalise_key(arg: str) -> str:
    """Accept a bare key, a path to the page, or a key with a .md suffix."""
    name = arg.strip().replace("\\", "/").rsplit("/", 1)[-1]
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name


def page_path(key: str) -> Path:
    return CONTENT_DIR / f"{key}.md"


def list_missing(challenges: list) -> None:
    missing = [c for c in challenges if c.get("key") and not page_path(c["key"]).exists()]
    width = max((len(c["key"]) for c in missing), default=20)
    for c in missing:
        day = str(c.get("day", "?")).rjust(2)
        lane = str(c.get("lane", "?")).ljust(11)
        web = f"web #{c['web_no']:<2} " if c.get("web_no") else ""
        print(f"{c['key']:<{width}}  day {day}  {lane} {web}{c.get('title', '')}")
    warn(f"{len(missing)} of {len(challenges)} catalog entries have no page in {rel(CONTENT_DIR)}/")


# --------------------------------------------------------------------------- template

def toml_string(value: str) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def toml_list(values) -> str:
    return "[" + ", ".join(toml_string(v) for v in values) + "]"


def toml_date(value) -> str:
    try:
        return _dt.date.fromisoformat(str(value)[:10]).isoformat()
    except ValueError:
        die(f"catalog date is not YYYY-MM-DD: {value!r}")


def strip_go_template(text: str) -> str:
    """Reduce a Hugo archetype to its static skeleton.

    Every {{ ... }} action is removed and every {{ if }} / {{ with }} / {{ range }}
    block is treated as false (a bare {{ else }} branch is kept), honouring the
    {{- and -}} whitespace-trim markers the way Go templates do. Shortcode
    escapes ({{< >}}, {{% %}}) are left alone for render_like_hugo_new().
    """
    out = []
    keep = [True]        # one entry per open block: is this branch kept?
    lstrip_next = False  # set by -}} : trim the whitespace after the action
    pos = 0
    for m in _ACTION.finditer(text):
        literal = text[pos:m.start()]
        pos = m.end()
        if lstrip_next:
            literal = literal.lstrip()
        if m.group(1):   # {{- : trim the whitespace before the action
            literal = literal.rstrip()
        if keep[-1]:
            out.append(literal)
        body = m.group(2)
        word = body.split(None, 1)[0] if body else ""
        if word in _BLOCK_OPENERS:
            keep.append(False)
        elif word == "else" and len(keep) > 1:
            keep[-1] = keep[-2] and not body[4:].strip()  # "else if" / "else with" is one more false condition
        elif word == "end" and len(keep) > 1:
            keep.pop()
        lstrip_next = bool(m.group(3))
    literal = text[pos:]
    if lstrip_next:
        literal = literal.lstrip()
    if keep[-1]:
        out.append(literal)
    return "".join(out)


def render_like_hugo_new(text: str) -> str:
    """Mimic the parts of `hugo new` that matter for a static stub."""
    text = _GO_COMMENT.sub("", text)
    text = strip_go_template(text)
    text = text.replace("{{</*", "{{<").replace("*/>}}", ">}}")
    text = text.replace("{{%/*", "{{%").replace("*/%}}", "%}}")
    return text


def split_front_matter(text: str) -> tuple:
    lines = text.lstrip("﻿ \t\r\n").splitlines()
    if not lines or lines[0].strip() != "+++":
        die("archetype must start with TOML front matter (+++ ... +++)")
    for i in range(1, len(lines)):
        if lines[i].strip() == "+++":
            return lines[1:i], lines[i + 1:]
    die("archetype front matter is not closed with +++")


def trailing_comment(rest: str) -> str:
    """Return the `  # comment` tail of a TOML value line, or '' (quote-aware)."""
    quote = None
    i = 0
    while i < len(rest):
        ch = rest[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#":
            start = i
            while start > 0 and rest[start - 1] in " \t":
                start -= 1
            return rest[start:]
        i += 1
    return ""


def find_key(fm: list, key: str) -> int:
    for i, line in enumerate(fm):
        m = _KEY_LINE.match(line)
        if m and m.group(2) == key:
            return i
    return -1


def value_of(line: str) -> str:
    """The value part of a `key = value  # comment` line, without the comment."""
    m = _KEY_LINE.match(line)
    rest = line[m.end():] if m else ""
    comment = trailing_comment(rest)
    return (rest[:len(rest) - len(comment)] if comment else rest).strip()


def set_key(fm: list, key: str, value: str, after: str = None, keep: bool = False) -> None:
    """Set `key = value` in the front matter, keeping the line's own comment.
    keep=True leaves an existing value alone and only adds the key if missing."""
    i = find_key(fm, key)
    if i >= 0:
        if keep:
            return
        m = _KEY_LINE.match(fm[i])
        comment = trailing_comment(fm[i][m.end():]).lstrip()
        sep = m.group(3).rstrip() + " "  # keep the alignment before "=", one space after it
        line = f"{m.group(1)}{key}{sep}{value}"
        if comment:
            column = len(fm[i]) - len(comment)  # the column the archetype keeps its comments in
            line = line.ljust(max(column, len(line) + 2)) + comment
        fm[i] = line
        return
    line = f"{key} = {value}"
    j = find_key(fm, after) if after else -1
    if j < 0:  # no anchor: stay top-level by going before the first [table] header, if any
        j = next((n for n, text in enumerate(fm) if _TABLE_LINE.match(text)), len(fm)) - 1
    fm.insert(j + 1, line)


def build_stub(template: str, entry: dict, depth: str) -> str:
    fm, body = split_front_matter(render_like_hugo_new(template))
    set_key(fm, "title", toml_string(entry.get("title") or entry["key"]))
    set_key(fm, "date", toml_date(entry.get("date")), after="title")
    set_key(fm, "draft", "true", after="date", keep=True)
    # Hugo >= 0.144 rejects a top-level "kind" in front matter; the params map keeps it
    # reachable as .Params.kind, which is what the section templates look up.
    k = find_key(fm, "kind")
    if k >= 0 and not any(_TABLE_LINE.match(text) for text in fm[:k]):
        m = _KEY_LINE.match(fm[k])
        fm[k] = f"{m.group(1)}params.kind{m.group(3)}{fm[k][m.end():]}"
    if find_key(fm, "kind") < 0:  # no kind inside a [params] table either
        set_key(fm, "params.kind", '"challenge"', after="draft", keep=True)
    set_key(fm, "catalog_key", toml_string(entry["key"]), after="params.kind")
    set_key(fm, "depth", toml_string(depth), after="catalog_key")
    # The archetype fills tags/skills from the lane under `hugo new`; do the same when it left them empty.
    lane_key = str(entry.get("lane") or "")
    for key, defaults in (("tags", LANE_TAGS.get(lane_key)), ("skills", LANE_SKILLS.get(lane_key))):
        i = find_key(fm, key)
        if defaults and i >= 0 and value_of(fm[i]) in ("[]", '""', "''", ""):
            set_key(fm, key, toml_list(defaults))
    # An unsolved challenge gets no attribution: the archetype's default would
    # otherwise claim the pipeline solved it. Say so in a TODO instead.
    if entry.get("solved") is False:
        set_key(fm, "solved_by", "[]", after="description")
        i = find_key(fm, "solved_by")
        if "unsolved in the catalog" not in fm[i]:
            fm[i] = fm[i].rstrip() + "   # TODO: unsolved in the catalog"

    web_no = entry.get("web_no")
    lane = entry.get("lane", "?")
    lane_label = entry.get("lane_label") or lane
    web_text = "none" if web_no is None else str(web_no)
    facts = [
        "# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):",
        f"#   day {entry.get('day', '?')} ({entry.get('date', '?')}), lane \"{lane}\" ({lane_label}), web_no {web_text}",
        f"#   gm_id {entry.get('gm_id', '?')}",
    ]
    at = find_key(fm, "catalog_key")
    for offset, line in enumerate(facts, start=1):
        fm.insert(at + offset, line)

    leftovers = [line for line in fm if "{{" in line]
    if leftovers:
        die("archetype front matter still contains Hugo template expressions this script "
            "cannot render; fill them by hand or simplify the archetype:\n  " + "\n  ".join(leftovers))

    return "+++\n" + "\n".join(fm) + "\n+++\n" + "\n".join(body).rstrip("\n") + "\n"


# --------------------------------------------------------------------------- main

def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):  # never crash on a console that cannot print a title
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        prog="ctf_new.py",
        description="Create a draft challenge page for the Huntress CTF 2026 section from the catalog.",
        epilog="Examples:\n"
               "  python scripts/ctf_new.py day06-pool-party --depth full\n"
               "  python scripts/ctf_new.py --list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("key", nargs="?", help="catalog key, e.g. day06-pool-party (a path or .md suffix is fine)")
    parser.add_argument("--depth", choices=DEPTHS, default="note",
                        help='"note" (default) for a short field note, "full" for a curated write-up')
    parser.add_argument("--list", action="store_true", help="print the catalog keys that have no page yet, then exit")
    parser.add_argument("--archetype", type=Path, default=ARCHETYPE_FILE,
                        help="archetype to fill (default: archetypes/huntress-ctf-2026.md)")
    args = parser.parse_args(argv)

    challenges = load_catalog()
    if args.list:
        list_missing(challenges)
        return 0
    if not args.key:
        parser.error("a catalog key is required (or use --list)")

    key = normalise_key(args.key)
    by_key = {c.get("key"): c for c in challenges if c.get("key")}
    entry = by_key.get(key)
    if entry is None:
        warn(f"no catalog entry with key {key!r}")
        close = difflib.get_close_matches(key, list(by_key), n=5, cutoff=0.5)
        subs = [k for k in by_key if key.lower() in k.lower() and k not in close][:5]
        if close or subs:
            warn("did you mean: " + ", ".join(close + subs))
        warn("run with --list to see the keys that still need a page")
        return 1

    target = page_path(key)
    if target.exists():
        warn(f"refusing to overwrite {rel(target)}; delete it first if you want a fresh stub")
        return 1

    if args.archetype.exists():
        template = args.archetype.read_text(encoding="utf-8-sig")
    else:
        warn(f"archetype not found at {args.archetype}; using the built-in fallback template")
        template = FALLBACK_ARCHETYPE

    stub = build_stub(template, entry, args.depth)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8", newline="\n") as fh:
            fh.write(stub)
    except FileExistsError:
        warn(f"refusing to overwrite {rel(target)}; delete it first if you want a fresh stub")
        return 1

    lane_label = entry.get("lane_label") or entry.get("lane")
    print(f"wrote {rel(target)}")
    print(f"  {entry.get('title', key)}  (day {entry.get('day', '?')}, {lane_label}, depth = {args.depth})")
    print("  next: write the prose, resolve the TODO comments, then set draft = false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
