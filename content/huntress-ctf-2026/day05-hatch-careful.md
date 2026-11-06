+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Hatch Careful"
date = 2026-10-05  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day05-hatch-careful"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 5 (2026-10-05), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-05-python-carrier-lab
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A tiny syntax-tree evaluator reads literals out of fourteen kinds of Python packaging without importing or running anything, because the decoded plan states its own labels."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "homebase"]

tools  = ["pysolve.py", "scriptsolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["malware-analysis", "python", "obfuscation", "deobfuscation"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 5 added Python: nine behaviours packaged in fourteen kinds of carrier (source, old and current bytecode, zipapp, wheel, frozen executables, PyArmor), 357 fields in all. Nothing hatches, which was the point.

## The solve

At release on 5 October the supervisor didn't submit, because no Python or VBScript solver existed yet. The Claude Code session then wrote `pysolve.py`, which walks each file's syntax tree with a small evaluator. It understands only literals, tuples and lists, string concatenation, `str.join`, `format` with literal dicts and `tuple()`; anything else yields nothing, so no code is imported or executed. It decodes the plan, and the plan states the syntax, obfuscation, carrier and Windows-chain labels outright. Role comes from the decoded steps, not the file name. That banked 343 of 357 the same day, and the Day 6 codecs lifted it to 346.

The VBScript control labels came from the event's Homebase AI (GPT-6 Luna), which also solved the mastery at 22:10:56 on 7 October. The single's last field, a Batch expansion, closed at 17:15:15 on 7 October. The time trial went in at 20:36:55 on 7 October and was found correct by 10 October. The notes don't say who made either submission.

The Python relay role is plain `relay`, unlike JScript, where the same role is `staged_chain`.
