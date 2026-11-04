+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Escape Room"
date = 2026-10-09  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day09-escape-room"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 9 (2026-10-09), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-09
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Unicode escape sequences needed one new decoder step, added in session by the agent, and a two-minute late pick-up of the release taught the scheduler to skip solved days."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py", "timed.py", "daily.py", "claude-code"]
tags   = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Another warmups blob, this time written in escape sequences: a quoted string of backslash-u escapes. Single and mastery both asked for the slug at the end of the decoded lines. The one new thing was the encoding; the mastery needed no new code.

## The solve

At release the supervisor had no decode for it and reported the single unsolved at 09:02:17. It had picked the day up two minutes late: the 08:50 run had re-confirmed the already-solved Day 8, because the marker was stale. In a Claude Code session the agent added a `unicode_escape` step to `wusolve.py`: `json.loads` when the text starts with a double quote, otherwise Python's `unicode_escape` codec, which also covers hex escapes. All three modes were CORRECT by the 09:25:00 commit; exact submit times aren't recorded.

`timed.py` maps each blob to its question by artifact name, so the mastery solved as soon as the single's encoding decoded. The Time Trial and mastery questions carried an appended artifact hash in their text, but the answer was still the slug alone.

`daily.py` now advances past any fully solved day.
