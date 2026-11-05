+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Out of Order"
date = 2026-10-28  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day28-out-of-order"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 28 (2026-10-28), lane "script" (Script Analysis), web_no none
#   gm_id script-analysis-day-28-terraform-cloud-timeline
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Terraform HCL polyglots at 1,703 fields: a cloud-timeline question set that the existing deterministic pipeline banked in all three modes within seconds of the release."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot"]

tools  = ["python"]
tags   = ["malware-analysis", "terraform", "time-trial", "mastery"]
skills = ["Malware Analysis"]  # groups it on /portfolio/

toc = false
+++

Day 28 brought Terraform HCL polyglots. The prompt asked for a cloud timeline assembled without planning or applying anything, and for the one change that happened out of order. The question shapes were the same as on the lane's earlier days.

## The solve

The autopilot banked all three modes at the release: the single at 09:00:08, the Time Trial at 09:00:11 and the mastery (twelve sets, 21,372 fields) at 09:00:21. The notes record it as fully automatic, with no new code.

This time the Time Trial carried 1,781 fields, a different set from the single's 1,703, with no ATT&CK-id fields.

That afternoon a ranked loop re-solved the Script Time Trial and mastery runs for several earlier days, this one included, as ranked attempts. The loop log puts that around 17:07 ET.

A deterministic lane does not care what the day's language is, as long as the declared formats stay put.
