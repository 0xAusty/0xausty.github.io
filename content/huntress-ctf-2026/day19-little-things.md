+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Little Things"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-little-things"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-19
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A hex-encoded UTF-16 blob failed the printable filter at release, and the pre-commit replay gate then caught two latent solver faults the live submits had hidden."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["wusolve.py","kpa.py","python"]
tags   = ["encoding","time-trial","mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Each blob was a run of numbered chunks, and Day 19's encoding decided the answer slug. The encoding itself was routine, hex of UTF-16LE text starting with a byte-order mark. Getting it into the solver took longer.

## The solve

At release the single stayed unsolved. Hex decoding produced bytes full of NULs, and the solver's printable-ASCII filter threw them away, so it never reached the text. Claude Code added a UTF-16 detector to `wusolve.py` (a byte-order mark, or an all-zero high or low byte plane) and two steps that use it. The single was fixed by 09:01:07, and the time trial and the 93-blob mastery were correct on their first submit.

Committing the fix was harder. The pre-commit replay gate re-solves every past case with the learned-key cache cleared, and it blocked the commit twice. The first time, the new steps were among the first-pass steps, so the beam stacked a second cipher on the UTF-16 output and flooded with junk slug tails, which regressed all 93 mastery chunks. A UTF-16 decode is terminal, so it now sits outside the first-pass set. The second time, a six-character slug chunk needed a three-rail rail fence, which had only ever been reachable through the cache. Bounded rail fence and columnar searches went into the always-tried steps in `kpa.py`.

The live submits were already right; what the gate protected was the next unattended run.
