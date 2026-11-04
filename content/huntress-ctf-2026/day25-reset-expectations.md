+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Reset Expectations"
date = 2026-10-25  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day25-reset-expectations"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 25 (2026-10-25), lane "web" (Web Exploitation), web_no 17
#   gm_id web-exploitation-day-17-reset-expectations
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "A password-reset token that was not bound to its account: a token issued for a self-service account could be redeemed against a privileged one."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation"]
skills = ["Web Application Security"]  # groups it on /portfolio/

toc = false
+++

This was a broken password-recovery flow with a request route that issues a reset token and a redeem route that spends it. The disclosed account ids included a self-service account and a privileged one. The flaw sat on the redeem step, not the request step.

## The solve

The redeem route never checked that the token had been issued for the account it was being redeemed against. So the solver requests a token for the self-service account, spends that same token against the privileged account, and gets that account's proof back. This is a sideways account takeover. Three parallel Claude Code subagents handled the day's web shapes, and this one became `solve_reset` in `websolve.py`. If the guide hides which account is the self-service one, the solver falls back to probing each listed id as the token source.

The single was correct by 09:08:17 on 25 October, the time trial by 09:08:29 and mastery by 09:08:40.

The token was genuine, which is why this is easy to miss in review: nothing was forged. The fix is to bind a reset token to the account and purpose it was issued for, and to check that binding at redemption.
