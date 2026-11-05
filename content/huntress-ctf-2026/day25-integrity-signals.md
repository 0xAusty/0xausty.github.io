+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Integrity Signals"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-integrity-signals"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-25-integrity-signals
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mastery came back 7 of 9 at release; the agent extended the emulator with switches, reflection and a branching x86 interpreter while a hot-reload supervisor retried on every save."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["mobsolve.py", "mobemu.py", "nativemix.py", "python"]
tags   = ["android", "emulation", "x86", "reflection"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 25 asked for the exact backend answer code per mode, with a prompt about forging or replaying a bounded integrity statement. The single and time trial were correct at 09:00:04 and 09:00:06. The nine-APK mastery mixed earlier mechanisms and came back seven of nine, and the supervisor banked the seven it was confident in.

## The solve

This was the hot-reload supervisor's first morning: each time Claude Code saved an emulator fix, the supervisor re-solved the affected modes within seconds. Each failure named the next gap. First a native call with two arguments and the packed-switch opcode. Then an unhandled x86 `cmp` and the check-cast opcode. Then an XOR on a value the emulator had not produced.

The agent's fixes in `mobemu.py` added packed and sparse switches, check-cast as a no-op, the `Long` helpers and Java reflection, resolved to a direct call on the named sibling method. `nativemix.py` went from a linear executor to an instruction-pointer interpreter with a flags model, because the Day 16-style set gated on a 16-bit compare. Set 6 cleared at 09:20:44 and the reload at 09:24:54 solved all nine; the mastery was accepted at 09:24:57.

Banking the confident sets first meant the fix only had to supply two.
