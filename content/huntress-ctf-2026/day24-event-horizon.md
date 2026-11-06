+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Event Horizon"
date = 2026-10-24  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day24-event-horizon"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 24 (2026-10-24), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-24-event-horizon
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The record-count question was easy, but a sleeping laptop and a filename bleed across Mastery sets stacked two failures on one morning."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["metaextra.py", "mfsolve.py", "python"]
tags   = ["evtx", "metadata", "forensics"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Day 24 asked for the record count of a Windows event log, as an integer. Two things went wrong at once: the laptop was off at 09:00, so the whole pipeline ran late, and the lane's oldest question type broke in the cumulative Mastery.

## The solve

The systemd timer caught up at 09:14:20, and the single and the Time Trial were correct on the first submit, at 09:14:31 and 09:14:33. The EVTX parser walks the 64 KiB chunks after the 4 KiB file header and sums each chunk's last-minus-first-plus-one record numbers. It exposes the file header's next-record counter as well, but doesn't trust it for the count.

Mastery came back incorrect. Its sets repeat stems such as `roster-*` and `evidence-note-*`, so a global member-name search bled one set's filename onto all of them, and seven filename fields were wrong. The grader rejected heal's uppercase re-spellings. The agent scoped the filename lookup to each set's own archive with a priority matcher. A first, naive scoping fix had regressed Day 1, whose note has no id suffix, which is why the matcher has a priority order. Mastery was correct at 09:28:19, with the seven ZIP member-name fields already healed to sorted order automatically.

Each missed single cascades into three modes, because the Time Trial is gated on the single and Mastery on the Time Trial.
