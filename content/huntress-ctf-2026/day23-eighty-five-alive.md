+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Eighty-Five Alive"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-eighty-five-alive"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-23
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Ascii85 was already in the solver, but the mastery left 14 of 113 sets unmapped, and a later fix exposed an Adobe-frame bug that dropped a byte."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot","agent"]

tools  = ["wusolve.py","timed.py","python"]
tags   = ["encoding","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

The alphabet got bigger, and "Adobe might recognize the neighbors" is a hint at Ascii85 with its angle-bracket framing. The notes do not name the encoding, so that is an inference from the prompt. The decoder had an Ascii85 step from its first commit.

## The solve

The single and the time trial were decoded by the pipeline at release. The mastery banked 99 of its 113 sets and left 14 unmapped after a solve of about a minute. A Claude Code session that later died finished the rest, and the mastery was confirmed by 09:11:31. How it finished the 14 is not recorded.

Two fixes came afterwards. On 28 October a commit traced Day 22 and 23 mastery stragglers to blobs whose chunk straddles the sentence and slug seam, where a rail-fence key learned in one worker never reached the others. It is likely, but not stated, that these were the same 14. On Day 24 the agent also found that the Ascii85 step stripped the Adobe frame before decoding, which drops the last byte. It decodes with the frame now, and one stored mastery golden was corrected.

Frame characters are part of the data: strip them and you can lose the last byte.
