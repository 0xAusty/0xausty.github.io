+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Dim and Dimmer"
date = 2026-10-04  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day04-dim-and-dimmer"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 4 (2026-10-04), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-04-shell-contrast
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Nine VBScript files decoded statically, where the hard part was matching the generator's short labels for control flow rather than the decoding itself."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["vbsolve.py", "scriptsolve.py", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["malware-analysis", "vbscript", "obfuscation", "xor"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 4 added nine VBScript files, taking the single to 231 fields: role, technique, adapter, campaign, the codec's representation and transform, the control-flow form of the `Recover_` function, and an indicator. The decoding was routine. The "winding control flow" was a vocabulary problem.

## The solve

`vbsolve.py` reassembles the `Material_` constant, converts it by the named representation (decimal with several separators, hex, base64), applies the named transform (reverse, XOR, add or subtract modulo 256, rolling XOR) and keeps the candidate that decodes to a valid descriptor. It labels the `Recover_` wrapper from the construct around it. The Claude Code session banked 215 of 231 on 5 October and 222 after the Day 6 codecs.

The grader wanted the generator's own short names, and several guessed names were rejected first. The label map that settled it came from the event's Homebase AI (GPT-6 Luna), and the session then encoded it. The same AI solved the mastery on 8 October. The time trial was found already correct on 10 October, and the notes don't say who submitted it.

An `If True Then` is transparent: label by the construct inside it. A byte-decoding `For` loop is not a wrapper. One Batch label was left unguessed under the no-brute-force rule.
