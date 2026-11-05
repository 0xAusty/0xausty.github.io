+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Protocol Reconstruction"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-protocol-reconstruction"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-28-protocol-reconstruction
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A hex-encoded binary frame whose prompt warned about nonce and ordering semantics: the fix was decoding the length-prefixed payload in frame order, never re-sorting."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "encoding", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked for the app-to-backend protocol to be reconstructed with its nonce and ordering semantics preserved. The puzzle turned out to be a new **packet** codec: a hex-encoded binary frame with the magic bytes `HA`, a length byte, the payload and a trailing nonce or control byte.

## The solve

The release run found nothing and was unsolved at 09:00:08. The plain hex path fails here, because the framing bytes make the decoded text differ from the answer code. Claude Code added a packet branch to `decode_puzzle` in `mobsolve.py`. It hex-decodes the frame, takes the length-prefixed payload after the magic and length byte, and reads the code from it in frame order. If that fails, it falls back to an order-preserving scan of the whole frame.

The prompt's phrase about ordering was the warning: never reverse or re-sort the payload. The supervisor's hot reload at 09:15:30 banked the time trial and mastery by 09:15:37, and the single was correct at 09:14:33. The notes do not say who submitted the single.

About 11 minutes were lost because recovery waited until I noticed the misses.
