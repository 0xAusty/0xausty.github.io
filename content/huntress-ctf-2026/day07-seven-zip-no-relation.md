+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Seven-Zip, No Relation"
date = 2026-10-07  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day07-seven-zip-no-relation"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 7 (2026-10-07), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-07-seven-zip-no-relation
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The answer is the entry count a ZIP's end-of-central-directory record claims, not the number of members present, so the solver reads the record instead of counting files."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["forensics", "metadata", "zip"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

Each mode asked for one integer: the total-entries field of a named inner archive's end-of-central-directory record. The single and time trial were plain; the mastery nested the archives two levels deep.

## The solve

The 09:00 sweep fetched the single and left it unsolved, and the time trial and mastery were not attempted. Claude Code then worked it in session. The handler finds the `PK 05 06` signature and reads the 16-bit total-entries value at offset 10. For the mastery, the lookup in `mfsolve.py` had to recurse from the outer zip into `evidence-0N.zip` and then into the named drop.

All three modes were CORRECT by 11:24 on 7 October, the time of the commit that reports them. The notes do not record the individual solve times.

The question wants the number the record claims. The agent's notes warn that this census does not always match the real file count, which is the forensic point of the challenge.
