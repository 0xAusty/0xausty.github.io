+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Layered Protections"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-layered-protections"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-30-layered-protections
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A search-based decoder peels composed layers to depth three and refuses to answer when two codes tie, banked about five minutes after release by an escalated agent."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "obfuscation", "deobfuscation", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked for obfuscation, native indirection, runtime decryption and integrity checks to be unwound while proving the same backend effect. The single's puzzle was a new **layered** codec: a blob wrapped in several composed layers, with a declared key. The recipe is written down nowhere, because the DEX keeps only constants.

## The solve

`mobsolve.py` peels the blob breadth-first. It starts from the base64, hex and raw readings and applies primitive steps up to depth 3: reverse, a 16-bit swap, and XOR, add or subtract with the key, the key plus the position, the key times the position or the position alone. The shallowest depth that yields a valid answer code decides, and only if the code is unique at that depth. If two differ, the decoder returns nothing rather than guess. Nothing is variant-specific, so a different key or layer order resolves the same way.

The fix came from a headless Claude Code agent that the supervisor launched on its own. It kicked the escalator, built the night before, at 09:00:31. Four reloads still left the single unsolved, and the reload at 09:04:54 banked all three modes by 09:05:06. The escalator then hit a Claude session limit at 09:07:26, after the fix had landed.

It was the escalator's first morning, and nobody launched recovery by hand.
