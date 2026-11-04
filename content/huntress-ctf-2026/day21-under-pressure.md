+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Under Pressure"
date = 2026-10-21  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day21-under-pressure"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 21 (2026-10-21), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-21
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Base64 and gzip wrapper needed one combined step, and the gate's failures blamed the new gzip change when a stripped space in a transposition window was the real cause."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py","kpa.py","python"]
tags   = ["encoding","base64","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The hint was a familiar wrapper with something compressed inside. The single was Base64 around a gzip stream. The day had two problems, and the obvious suspect for the second was innocent.

## The solve

At release the single stayed unsolved. Claude Code added a decompress step to `wusolve.py` that picks gzip, bz2, xz or zlib by magic bytes, plus a combined Base64-then-decompress step. It had to be combined: Base64's output here is unprintable, and the chunk search does not recurse into unprintable text.

Then the replay gate flagged four keyed-transposition slug chunks. The gzip change was the first suspect, and it was not the cause. In the mastery, some fixed-width sentence windows carry a rail-fence or columnar transposition that includes a leading space. The bounded transposition search in `kpa.py` had been run on the stripped token with spaces gated out, so the first slug word came out scrambled. The fix was to search the raw chunk and allow a space in the gate. The replay then showed no regressions across the warmups and mobile cases.

The time trial and mastery were solved by 09:10:59, after the single was fixed.

Stripping whitespace before a transposition search quietly changes the length it has to fit.
