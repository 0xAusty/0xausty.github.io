+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Power Play"
date = 2026-10-01  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day01-power-play"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 1 (2026-10-01), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-01-native-signals
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Three PowerShell samples hide their indicators in a base64 JSON blob, so a shape-matching decoder reads them statically and refuses to answer when two values fit."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []

tools  = ["scriptsolve.py", "aeszip.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["malware-analysis", "powershell", "base64", "mitre-attack"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

The first Script Analysis challenge gave me three PowerShell samples and asked for a scenario label, the primary ATT&CK technique and a handful of exact indicators from each. It is routine: every sample carries its configuration as a base64-encoded JSON literal, so nothing needs running.

## The solve

`scriptsolve.py` decodes the JSON and picks each indicator by its shape: a URL, a wallet prefix, a mutex name, a user-agent string, a leading-dot extension, a recovery-note filename. It answers only when exactly one decoded value fits, and otherwise declines. Scenario and technique come from a fixed per-sample table. The evidence zip is encrypted with the usual malware-sample password, and `aeszip.py` opens it.

The notes do not record who solved Day 1 or how. The laptop pipeline didn't exist yet, and the earliest work ran through other tooling. What I can say is that the solver encodes the family as it stood by 5 October. The catalog's three timestamps are one second apart, which looks like a state sync, so I give no solve times.

These fifteen fields came back inside later cumulative challenges. On Day 23 they returned under opaque ids, and the grader settled that the collection sample's "first filename" means the first entry of the decoded file list, not the separate archive name.

The archive name was the decoy; the first list entry was the answer.
