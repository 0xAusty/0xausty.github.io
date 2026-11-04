+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Host With the Most"
date = 2026-10-02  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day02-host-with-the-most"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 2 (2026-10-02), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-02-encoded-intent
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "JScript samples were read safely by running only their inert decode function inside an empty Node sandbox, with style labels taken from a second function's syntax."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["jsan.js", "scriptsolve.py", "node", "python"]                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = ["malware-analysis", "jscript", "nodejs", "obfuscation", "time-trial"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 2 added nine JScript files to the PowerShell set. Each file asks for a role, a technique, three style labels (function, invocation and property-access style) and indicators from the decoded configuration. The interesting part was reading hostile script without running it.

## The solve

`jsan.js` loads each file into an empty Node `vm` context, where no Windows Script Host objects exist and a one-second timeout applies. It calls only the inert `recover_*` function, parses the JSON it returns, and reads the `inspect_*` function's syntax with regexes: declaration or named or anonymous expression, direct or `.call` or `.apply`, dot or bracket access. `scriptsolve.py` maps role and technique. Later a warm `node jsan.js --serve` process removed Node's start-up cost for the timed modes.

The notes credit the time trial and mastery to the Claude Code laptop session of 4 October. The single was accepted by 2 October, but the notes don't say whose solver did it, and I don't claim it.

That day also taught a timing lesson. A sweep opened all five time trials before analysis was ready, and the 5 to 8 second timers expired.

Prepare the decoding before you open a timer.
