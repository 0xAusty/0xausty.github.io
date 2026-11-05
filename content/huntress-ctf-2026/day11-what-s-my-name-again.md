+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "What’s My Name Again?"
date = 2026-10-11  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day11-what-s-my-name-again"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 11 (2026-10-11), lane "metadata" (Metadata Forensics), web_no none
#   gm_id metadata-forensics-day-11-whats-my-name-again
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The answer is the original filename declared inside a PE's version resource, not its on-disk name; a nested-zip lookup bug was caught offline before the only retry was spent."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["mfsolve.py", "python"]
tags   = ["forensics", "metadata", "pe", "mastery"]
skills = ["Digital Forensics"]  # groups it on /portfolio/

toc = false
+++

The executables had randomised on-disk names, and each mode asked for the original filename the binary declares in its version resource. The file lies about its name, which is a real malware-triage tell.

## The solve

The release sweep left it unsolved. A fresh session then ran one Claude Code subagent per lane that was not fully CORRECT, and metadata was the only lane needing new code. The agent wrote a static reader in `mfsolve.py`: section table, `.rsrc`, the version resource, then the UTF-16 string pairs, each DWORD-aligned. The answer id suffix is matched to the resource's own key name, so other keys resolve without a table. The commit is stamped 09:15; the scoreboard puts the single at 09:11:34, the time trial at 09:11:44 and the mastery at 09:14:36.

The first mastery submit scored incorrect. The member lookup searched only the outer zip, so both sets were answered from set 1's executable.

With one retry left on a timed mastery, the agent verified the fix offline on the saved expired artifact, against three artifact-string forms, before spending it. When retries are scarce, prove it on the bytes you already have.
