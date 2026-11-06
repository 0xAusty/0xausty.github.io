+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "The Butler Did It"
date = 2026-10-20  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day20-the-butler-did-it"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 20 (2026-10-20), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-20-jenkins-pipeline-intrusion
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A Jenkins Pipeline day about controller versus agent semantics, cleared in all three modes at the 09:00 sweep with no code change."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = []
tags   = ["malware-analysis", "groovy", "jenkins", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Jenkins Groovy polyglots with classic and Jenkins hosts and two bash fixtures, 1,329 fields in the single. The prompt asked to separate controller from agent semantics in a Jenkins Pipeline. It was a routine day.

## The solve

The cron sweep at 09:00:19 counted nine modes solved automatically across the lanes, and this lane's three were among them. The single, Time Trial and Mastery went in at 09:00:04, 09:00:07 and 09:00:11. No script code change is recorded for the day.

The pipeline did what it did on every other routine day: it read the descriptor out of each carrier, answered the fields, and submitted the single, then the Time Trial, then the Mastery. The notes hold no gotcha and no dead end for this challenge.

There's nothing to flag here. The pipeline solved it on its own.
