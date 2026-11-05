+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Jack in the Box"
date = 2026-10-19  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day19-jack-in-the-box"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 19 (2026-10-19), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-19-static-unpacking
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Day 19's challenge text spelled out its overlay packer, so the solve was transcribing a rotate-and-xor unpack faithfully and checking it against the stored SHA-256 before trusting the config."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["binsolve.py", "python"]
tags   = ["reverse-engineering", "elf", "xor", "time-trial", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = false
+++

Day 19 hid the HCFG config inside a packed overlay at the end of an ELF. Two new overlay fields appeared, the offset of the overlay magic and the overlay size, and many questions started to read as explicit instructions. This one spelled out the whole unpack.

## The solve

At release 220 of 228 fields were banked. The eight misses were the config fields, its version and the two overlay fields. The question described the format: find the last `PK19` marker, read two one-byte keys, a packed length and a SHA-256 of the unpacked bytes from the header, then unpack each byte as a rotate-right-by-3 of the byte XORed with the second key, XORed with the first key. The HCFG sits at offset 0 of the result.

Claude Code transcribed that into `binsolve._overlay`, which uses the unpacked HCFG only when its SHA-256 matches the stored digest. The overlay size is the member length minus the overlay offset. The single was fixed in session and correct by 09:02:41; the time trial and mastery followed on the first submit by 09:03:52, and the day was 15 of 15 by 09:05:18.

The static unpack needed no execution: the overlay's own header was enough to reverse the packer.

Take the last `PK19`, and verify the digest before believing the output.
