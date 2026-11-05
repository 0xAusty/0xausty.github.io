+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Cleartext Session"
date = 2026-10-08  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day08-cleartext-session"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 8 (2026-10-08), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-08-cleartext-session
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Mobile Day 8 was a routine solve by the existing solver; the trouble was a cron that never fired because the laptop was asleep."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mobsolve.py"]
tags   = ["android", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 8 asked for a backend answer code after recovering a synthetic session from allowed cleartext traffic. It was routine for the solver, which needed no change.

## The solve

The existing `mobsolve.py` handled all three modes as it was. The schedule was the problem. The 08:50 cron never fired on 8 October because the laptop was in S3 suspend, and a plain user cron doesn't run jobs it missed while the machine sleeps. So Claude Code ran the lanes by hand in the session. In the notes "by hand" means run manually instead of by cron, and the answer still came from the solver.

The single was accepted at 09:03:43, and the time trial and mastery at 09:25:12 and 09:25:15, all on 8 October. The next morning's 08:50 run only re-confirmed a state that was already CORRECT.

This was also the first day the time trial and mastery came back untimed, with no deadline from the Game Master. The timers returned on Day 10.

The missed cron led to the later fixes: a self-healing day marker, several idempotent retry slots and a persistent systemd timer.
