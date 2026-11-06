+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "No Artifact Left Behind"
date = 2026-10-31  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day31-no-artifact-left-behind"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 31 (2026-10-31), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-31-no-artifact-left-behind
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Rebuilding an artifact chain from each file's metadata: one root, one path to a done marker, and a decoy loop that a greedy regex turned into a fake chain."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["metaengine.py", "daily.py", "python"]   # shown at the bottom + browsable
tags   = ["forensics", "metadata", "sqlite", "png"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = true
+++

The last Metadata Forensics single of the month was the lane's hardest reasoning question. A case zip held artifacts that each name the next in their own metadata, and the answer was the ordered ids of the real execution-and-delivery chain, with a decoy loop beside it. It's worth writing up for two reasons. The one parsing bug on record turned that loop into a fake chain, which is the mistake the prompt warns against, and the last morning went wrong in four separate ways.

## The challenge

The single asked for one JSON field, `graph.execution_chain_artifact_ids` for `case-001.zip`: an array of ids in chain order, with `trim` the only declared normalisation. Since Day 3 every new question in the [Metadata Forensics lane](/huntress-ctf-2026/lanes/metadata/) had read `Determine <format>.<field> for <member>.`, and this one kept the pattern with a format token no parser knew: `graph`.

The time trial and mastery were the lane's cumulative inventory, the earlier days' questions asked again; the mastery, in fifteen sets, was the lane's largest bundle. Each mode was gated on the one before.

## Reading the prompt

The prompt describes the graph, clause by clause.

| Phrase | Implication | What the solver did |
|---|---|---|
| "Everything is evidence now" | Any artifact can be a link, whatever its format. | `parse_graph` makes every member of the case zip a node and searches its raw bytes. |
| "complete execution-and-delivery chain" | One ordered path from start to finish. | Each artifact gets one outgoing edge; the walk runs from the root to the end. |
| "defend every edge with primary metadata" | Each link must be named in the artifact's own content. | An edge is the first other known id in the artifact's bytes, with base64 email attachments decoded. |
| "the tempting conclusion the corpus does not support" | Something is built to look like the answer. | The chain must start at the one artifact nothing references; the leftover loop is returned as `cycle_artifact_ids`. |

The single asked only for the chain, so the loop never had to be named.

## What was in the files

`case-001.zip` held artifacts named by their ids: a codename, a hyphen and a hex suffix. The comment above `parse_graph` lists where each one names the next:

| Artifact | Where it names the next one |
|---|---|
| PowerShell script | the path given to `Invoke-Item` or `Start-Process` |
| PNG | a `tEXt` chunk reading `next=` |
| SQLite database | a row in a `launch_queue` table |
| Inner zip | the `execute` line of its `run.txt` |
| Email | a base64-encoded route note ("forwarded to:", "open:") |

One PNG carries a done marker and points nowhere. The real chain starts at the only artifact that nothing points to and ends at that marker. Everything else forms a large loop with no origin and no end: in the parser's own words, "the tempting conclusion the corpus does not support".

## The solve

The laptop booted late on the last morning, at about 08:52, and preflight passed at 08:54:22. The supervisor saw the release at 09:00:04 and opened the single:

```text
[2026-10-31 09:00:04] discovered 21 released challenge(s), including 6 web mode(s)
metadata-forensics-day-31-no-artifact-left-behind start: open
 ids ['d31-case-001-graph-execution-chain-artifact-ids'] deadline None sol {} t+0.90s
 NOT COMPLETE (unmapped): 1 ['d31-case-001-graph-execution-chain-artifact-ids']
...
[2026-10-31 09:00:20] metadata-forensics-day-31-no-artifact-left-behind: unsolved
```

No parser knew the `graph` format yet, so nothing was submitted. At 09:01:34 the supervisor logged its first-pass misses (binary, metadata and web) and kicked the escalator, a headless Claude Code run that started at 09:01:38 and launched five agents in one turn. For the last two mornings I had opted every missed lane into this, deterministic ones included, even though I planned to be at the laptop. One agent took this challenge with the `det-solver.md` playbook: adapt the lane solver to the new shape, submit the single, then fold the fix in so the supervisor banks the timed modes.

The single was CORRECT by 09:10:58, its one recorded attempt. Who submitted it isn't recorded; the recovering session's notes say only that "the prior agent added `parse_graph`". Two things broke that morning. The escalator was killed at its 600-second background-wait ceiling, taking all five agents with it, and the Claude Code session coordinating the morning crashed mid-task.

The session that recovered the morning restarted keep-awake, solved the deterministic misses inline, sent three fresh agents after the web and binary ones and fixed `parse_graph`'s edge extraction. The first version found edges with a greedy pattern for anything id-shaped, `[a-z]+-[0-9a-f]{3,}`. A SQLite row packs its target id and a note with no separator, and the note began with *amber*. The pattern ran on into the *a*, a hex digit, and produced an id that doesn't exist.

{{< callout type="warning" title="A loop with one edge missing is a chain" >}}
Drop one edge from a loop and it becomes a path, with a start that nothing points to and an end that points nowhere: the shape of the real chain. One overrun id turned the decoy cycle into a fake chain.
{{< /callout >}}

The fix asks which known ids appear, not what looks like one, and takes the earliest:

```python
t = _graph_ref_text(data)
refs = [r for _, r in sorted((t.find(r), r) for r in ids if r != nid and r in t)]
edge[nid] = refs[0] if refs else None          # one outgoing edge; none -> terminal ("done")
```

The greedy pattern survives in the file as `_GRAPH_NODE_RE`, a constant nothing uses.

## Making it deterministic

`parse_graph` went into `metaengine.py` like every other format, registered as the `graph` parser with `evidencegraph`, `evidence_graph`, `casegraph`, `chain` and `corpus` as aliases. The engine's existing plumbing did the rest, down to rendering compact JSON; its docstring's rule is "New day -> add the field to its format's parser". The chain also comes back as delivery chain ids, length, root and terminal, so a field asked under any of those names resolves. The walk runs only when exactly one artifact has no predecessor, and everything off the chain goes into the loop list:

```python
targets = {t for t in edge.values() if t}
roots = sorted(n for n in nodes if n not in targets)
chain = []
if len(roots) == 1:                                # the supported chain: unique root -> terminal
    cur, seen = roots[0], set()
    while cur and cur not in seen:
        seen.add(cur); chain.append(cur); cur = edge.get(cur)
cycle = sorted(n for n in nodes if n not in set(chain))   # the unsupported residual loop
```

The fix went into commit `7fff503` at 09:45:03 with the morning's other fold-ins. The pre-commit replay gate re-solved 691 recorded attempts in 577s, 0 regressed and all 13,632 metadata fields matching, with learned keys cleared so that every answer came from the bytes and the prompt alone.

## Timed modes

Gating meant the supervisor opened only the single at 09:00. The plan was fold-in-first: the agent saves its fix, and the supervisor's hot reload re-attempts the next modes within about 10 to 30 seconds. The reload never came. The supervisor reloads solvers and opens new work only when no worker is running, and a warmups mastery worker stuck in the old `wusolve.py` deep search pegged a core from 09:00 and kept every lane from reopening. `daily.log` is silent from 09:03:36 to 09:38:06, and at 09:40 the supervisor was stopped at my request: "just kill it, no more drops".

The corpus holds one attempt per mode, a time trial at 09:15:28 and a mastery at 09:17:45, both stored as unsolved. Neither appears in the supervisor's log, and the notes don't say who ran them. The time trial was CORRECT at 09:17:09 and the mastery at 09:19:19, well before the 11:58:29 `daily.log` summary that lists only two modes still open, neither of them these.

## Dead ends

- **A greedy pattern for edges.** It read one character past an id in a packed SQLite row and broke the decoy loop into a chain. Replaced by exact matching of the known ids.
- **Leaving the timed modes to the supervisor.** The reload waited behind a stuck warmups worker. The same commit added `base64+decompress` and `decompress` to the first steps in `wusolve.py`, so that chunk now resolves in about 0.35s. The reload gating and the escalator's 600-second ceiling were found that day and not fixed, since it was the last release.

## Takeaways

1. **The decoy was structural.** The unsupported conclusion was a loop with no origin and no end, so the test that mattered was the shape: one root, one path to the done marker, the leftover reported apart.
2. **Match the identifiers you know.** The valid ids were known in advance, and a pattern for anything id-shaped still read one character too far and gave the decoy the shape of the chain.
3. **One scan stood in for five parsers.** Every edge was an id, so a search of each artifact's raw bytes replaced a reader per channel. The cost is the check the prompt asks for: the scan can't tell an id in the defending channel from one anywhere else in the file.
4. **Recovery paths fail too.** The escalator, the coordinating session and the supervisor's reload all failed on the last morning. The single still landed and the timed modes were CORRECT before noon, but not by the route the playbook planned.
