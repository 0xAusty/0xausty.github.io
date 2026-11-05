+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "White Box Key Recovery"
date = 2026-10-29  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day29-white-box-key-recovery"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 29 (2026-10-29), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-29-white-box-key-recovery
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A white-box crypto prompt that reduced to known plaintext: the fixed four-character answer prefix pins the intercept and slope of an affine per-position key."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent", "autopilot"]

tools  = ["mobsolve.py", "python"]
tags   = ["android", "xor", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

The prompt asked for an equivalent key operation to be recovered from challenge-owned table transformations. It sounds like heavy crypto. The single's puzzle was a new **table** codec: 20 hex-encoded bytes, the length of an answer code, and a declared scalar key.

## The solve

The per-position tables are equivalent to an affine operation, where each byte is the plain byte plus (key + step * position) mod 256. Every answer starts with the same known four-character prefix, so the first four bytes pin the intercept and the slope, and the declared key is the intercept. A decode is accepted only if all 20 bytes form a valid code. As a fallback, `_table_decode` in `mobsolve.py` takes the declared key as the intercept, tries slopes from -32 to 32 and accepts only a unique valid code. Nothing is hard-coded per variant.

Three supervisor attempts had returned nothing at release and after two reloads. Claude Code submitted the single itself in the recovery session, outside the supervisor, at 09:11:00, and the supervisor then banked the time trial and mastery itself by 09:11:09.

The answer format supplied the known plaintext. That the miss waited for a human is why the escalator was built that night.
