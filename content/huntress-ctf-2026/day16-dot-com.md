+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Dot Com"
date = 2026-10-16  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day16-dot-com"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 16 (2026-10-16), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-16
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Morse spelling hex fell past a 400-wide breadth-first frontier in the single path, so the right decoder existed but was never reached; a fuzzer followed."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py", "wufuzz.py", "timed.py", "python"]
tags   = ["encoding", "morse", "time-trial", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 16 was the first two-step single: Morse code that spells hex, which spells the sentence. Both decoders already existed, but the search never got to use the second one.

## The solve

The single-blob path called only `wusolve.solve_bytes`, a breadth-first search that keeps 400 candidates per level. Morse sits near the end of about 30 transforms, so its hex child fell past the cap. At release the single spent 13.65s with no answer, and the time trial and mastery were not attempted.

Claude Code fixed it in session. The line-oriented `solve_lines` decodes this blob in 0.01s, so single and time trial blobs now go through `solve_text`, which tries `solve_lines` first and `solve_bytes` second. All 66 historical single and time trial blobs still matched their goldens. The zip mastery already used `solve_lines` and was CORRECT unchanged. The single was in at 09:01:38, the time trial at 09:02:35 and the mastery at 09:02:59.

The follow-up was `wufuzz.py`, which encodes the sentence with every encoder, every ordered pair and sampled triples, then runs the timed single path. Pair failures went from 16 of 445 to 0.

A fixed-width frontier silently drops the children of late decoders, so order and width decide what is reachable.
