+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Loaded Later"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-loaded-later"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-20-loaded-later
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Another static-decode mobile day banked at release; the secondary-DEX mechanism it introduced returned on Day 31 as the one mastery set the emulator could not run."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "dex"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 20 asked for the exact backend answer code for a case and app package, one `answer` field per mode. The prompt was about analysing a challenge-signed secondary DEX and recovering the module contract. It was routine for the pipeline, and I had nothing to do with the solve.

## The solve

`daily.py` solved and submitted the single, the time trial and the five-APK mastery through `mobsolve.py`'s static decode. All three modes came back correct, and the supervisor's summary is stamped 09:00:19. As with the neighbouring days, the notes do not say which codec the puzzle used.

The mechanism came back on Day 31, where one mastery set was a Day 20-style app that loads a second DEX from its assets at runtime. It was the only set the emulator reported as not complete, until it learned to load a second DEX.

The release morning was routine, and the same shape tripped the emulator eleven days later.
