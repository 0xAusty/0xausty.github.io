+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Monkey Business"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-monkey-business"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-27
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Ook! is Brainfuck spelled in token pairs; the decoder the agent had added the afternoon before meant all three modes banked within seconds of release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["wusolve.py", "python"]                        # e.g. ["python", "binsolve.py"]: shown at the bottom + browsable
tags   = ["encoding", "brainfuck"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = false
+++

Day 27's warmup was an Ook! blob, which is Brainfuck with each command spelled as a pair of `Ook.`, `Ook?` or `Ook!` tokens. The single was the largest of the warmups singles. It was routine only because the decoder already existed.

## The solve

The `ook` step in `wusolve.py` maps token pairs to Brainfuck commands and reuses the Day 26 interpreter. It only runs when the text is nothing but Ook tokens in pairs. The agent (Claude Code) had added it the afternoon before as a guess at the generator's next move, with the commit message "Extends the Day-26 Brainfuck family ahead of release".

The guess was right. The pipeline's autopilot solved the single at 09:00:08, the Time Trial at 09:00:14 and the Mastery at 09:00:18, and the agent's session notes put every deterministic lane as banked by 09:00:46.

Because the next likely shape was covered the day before, there was nothing to fix at release.
