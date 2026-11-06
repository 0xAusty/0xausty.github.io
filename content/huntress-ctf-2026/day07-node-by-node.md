+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Node by Node"
date = 2026-10-07  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day07-node-by-node"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 7 (2026-10-07), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-07-node-operation-graphs
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Node.js operation graphs decoded with a shared regex-based decoder; an adapter named systemd whose path was a cron path meant cron persistence."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["nodesolve.py", "bashsolve.py", "scriptsolve.py", "vbsolve.py"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["malware-analysis", "nodejs", "bash", "obfuscation"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 7 added eight Node.js operation graphs and two "advanced Bash syntax" fixtures, 469 fields in total. Decoding was routine; two analyst-style tells were not.

## The solve

At release on 7 October the single was unsolved. The Claude Code session wrote `nodesolve.py`, which pulls the `Material_` and `Codec_` literals out with an escape-aware regex, un-escapes them, and reuses the Bash decoder, checked against the descriptor marker. New codec spellings went into the shared decoder. It reached 459 of 469 that day. The Batch loop label and the VBScript label map, which came from the event's Homebase AI (GPT-6 Luna), were then encoded, and the single was fully correct at 11:47:01 on 7 October. The same AI solved the mastery at 22:16:08 on 7 October. The time trial went in at 17:41:54 on 7 October.

The tells: a Node persistence adapter called itself systemd, but its schedule path was a cron path, so the technique is cron. And for a staged chain that dispatches a process, the technique is the interpreter, even when the config also names a cron path or a service.

The Batch loop wrapper was a red herring: dozens of compound names failed before the simple canonical label stuck.
