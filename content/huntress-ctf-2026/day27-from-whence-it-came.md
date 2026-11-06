+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "FROM Whence It Came"
date = 2026-10-27  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day27-from-whence-it-came"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 27 (2026-10-27), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-27-docker-build-attribution
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Dockerfile polyglots at 1,659 fields: the same deterministic script pipeline solved all three modes at the release, with no new solver code for the day."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python"]
tags   = ["malware-analysis", "docker", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 27 added Dockerfile polyglots to the Script Analysis lane. The questions were the usual long run of fields about the specimens' build stages, semantics and hand-offs, plus a few ATT&CK-id fields. For the pipeline it was routine.

## The solve

The autopilot solved all three modes at the 09:00 release: the single at 09:00:06, the Time Trial at 09:00:10 and the mastery (eleven sets, 18,249 fields) at 09:00:21. No new solver code was needed, and the notes record the day as fully automatic.

The one oddity was the Time Trial. It reused the single's question set, 1,659 fields with the ATT&CK-id fields, instead of the hex-id set that every Time Trial since Day 23 had used. The pipeline took that in its stride.

Nothing went wrong. The work had happened on earlier days, and this one only collected it.
