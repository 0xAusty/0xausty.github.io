+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Serialized Offender"
date = 2026-10-26  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day26-serialized-offender"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 26 (2026-10-26), lane "web" (Web Exploitation), web_no 20
#   gm_id web-exploitation-day-20-serialized-offender
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An unsigned serialised session let the client choose its own role; the fix is integrity protection and server-side authority over roles, which the solver confirmed live."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["python", "websolve.py"]
tags   = ["web-exploitation", "deserialization", "python"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

Each variant asked for one proof from a live target; mastery was a bundle of four. The weakness is old and high-impact: the session travels as a serialised blob with no signature, and the server believes whatever role is inside it.

## The solve

The target disclosed a state-format route that gave the request field, the encoding and a sample state, all randomised per attempt. `solve_serialized` in `websolve.py` reads those live, decodes the sample, raises the role value, re-encodes it and sends it back. The reply carries the proof.

Claude Code folded this in after a parallel helper subagent solved it on release morning. The single first showed as unsolved on the 09:00 pass, which was expected: it was a brand-new web shape with no solver yet. It was CORRECT at 09:01:58, the time trial at 09:03:21 and mastery at 09:03:45.

The prompt's phrase "sign nothing" was literal. The fix is to sign or encrypt session state, or better, keep the role on the server and send only an opaque session id.
