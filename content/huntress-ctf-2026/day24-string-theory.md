+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "String Theory"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-string-theory"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-24
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Run-length tokens joined by commas, where the separator can also be the character being counted, so the parser had to read count and character pairs and verify by round trip."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py","python"]
tags   = ["encoding","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The hint was to count carefully, because the comma knows where to stop. The blob was run-length data: tokens of a count, a colon and a character, joined by commas. The catch is that the character itself can be a comma, and a trailing comma is allowed.

## The solve

The 09:00 run didn't start on time. The laptop was off and the systemd timer caught up on wake, so the supervisor saw the release at 09:14:31. The single was unsolved at first and correct by 09:18:32. The time trial was correct at 09:34:19 and the mastery by 09:39:17.

Claude Code added a run-length step to `wusolve.py`, in the first-pass steps. It splits on count and character pairs instead of on commas, and it only fires when the text round-trips exactly through its canonical re-encoding, which keeps it from matching ordinary text by accident.

The same session found a latent Ascii85 bug that had been there since the first committed decoder. The step stripped the Adobe frame before decoding and dropped the last byte, which had left one stored golden answer wrong. That answer was corrected.

When the separator can also be data, read the count and character pairs and check the round trip.
