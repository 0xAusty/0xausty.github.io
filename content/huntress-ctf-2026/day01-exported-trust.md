+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Exported Trust"
date = 2026-10-01  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day01-exported-trust"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 1 (2026-10-01), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-01-exported-trust
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "An early Android challenge that looks like a runtime task but hides its answer code in a static asset: a plain decode, with no record of who solved it."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []

tools  = []
tags   = ["android", "encoding", "time-trial"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

This was the first mobile challenge. The prompt talks about invoking an exported deep-link Activity, but the notes say the early APKs never needed a device. Each one carries its answer code in `assets/huntress_puzzle.json`, in a new encoding every day, and Day 1's is the plain one, so this was routine.

## The solve

The notes don't record who solved Day 1, but the scoreboard records when: the single at 21:50:08 on 1 October, then the time trial at 09:30:07 and the mastery at 09:30:49 on the morning of 2 October. The only thing my notes have on it is a status sweep on 4 October that found all three modes already correct.

What they do describe is a static read. Open the APK as a zip, read the puzzle file and decode its `data` field by the declared `codec`. For the plain codec the data is the code itself. The committed `mobsolve.py` only accepts it as a whole-string match of the answer-code shape, which guards against submitting a half-decoded guess. Mastery APKs were solved in delivery order and paired with the set ids.

That method is reconstructed from those notes and the later solver, not from a solve log.

The prompt described runtime behaviour, but the answer was sitting in an asset file.
