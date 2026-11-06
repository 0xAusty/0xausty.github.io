+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Trust the Process"
date = 2026-10-14  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day14-trust-the-process"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 14 (2026-10-14), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-14-msbuild-trusted-project-abuse
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A routine MSBuild-polyglot day that the pipeline cleared at release, with a capped second try for the few batch-expansion fields that need one."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "msbuild", "batch", "bash"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

This was a routine day: MSBuild project polyglots plus two bash fixtures, 971 fields in the single. The prompt asked where a trusted toolchain ends up doing untrusted work, but the fields were the usual descriptor shape.

## The solve

The pipeline solved all three modes on its own at release. The only special handling was a capped second try for the FOR-expansion fields, the ones where the first spelling of an answer can be rejected: four in the single, four in the Time Trial and eight in the Mastery. The log shows the two-try batches for all three modes coming back correct, and the supervisor's summary at 09:00:40 had all three correct, 38 seconds after the release was seen.

Nothing new came out of the day. The two-try rule was already in place, and it held.

On a routine day, the work from earlier in the month does the solving.
