+++
title = "By the Numbers"
date = 2026-10-05
draft = true
params.kind = "challenge"
catalog_key = "day05-by-the-numbers"
depth = "note"
featured = false
description = "Decimal byte values, and the first morning of the cron runner: it banked two modes quickly but only after waiting for the wrong day's release."
solved_by = ["autopilot", "agent"]
tools = ["wusolve.py", "daily.py", "python"]
tags = ["encoding", "time-trial", "mastery"]
skills = ["Automation & Tooling"]
toc = false
+++

Day 5 is decimal byte values, hinted by "reduced to numbers", and it was the first morning the cron runner (`daily.py`) ran. The cipher was routine. The release timing was not.

## The solve

Day 5 was released before 09:00, and the runner was waiting for the wrong day. It saw the release at 09:05:15, and the single and the time trial were both correct by 09:05:27, the run's summary time. The submits themselves returned CORRECT 1.65 s into the single and 1.54 s into the time trial. `wusolve.py` handles the decimal step by turning numbers below 256 into bytes.

The mastery went worse. The run decoded only 2 of 23 blobs, and under the rule to submit only when every answer is solved, it submitted nothing. Why the per-chunk search failed on the other 21 is not recorded. The mastery was complete by the 11:19 handoff commit that morning, so I put it down to that Claude Code session, but no note says how it was fixed.

The fix for the early release was remembering the last processed day and polling every 10 seconds.
