+++
title = "Half a Turn"
date = 2026-10-02
draft = true
params.kind = "challenge"
catalog_key = "day02-half-a-turn"
depth = "note"
featured = false
description = "A trivial ROT13 warmup whose first time trial taught two lessons: the timer was too short for live analysis, and a retry served a different artifact."
solved_by = ["agent"]
tools = ["wusolve.py", "python"]
tags = ["encoding", "rot13", "time-trial"]
skills = ["Automation & Tooling"]
toc = false
+++

The cipher here is ROT13, hinted by "thirteen steps forward", and it is trivial. The time trial on 2 October taught the lessons behind the one-process runner.

## The solve

For the single, the scoreboard puts the correct submit at 12:51:07 on 2 October. My notes only mention it in a handoff written by a chat AI session, so who solved it is not recorded. The time trial and mastery were solved in the 4 October Claude Code session. For the mastery, `wusolve.py` decodes each chunk separately and keeps only readings that match the known sentence prefix and contain dictionary slug words, because a ROT13'd slug still looks like a slug.

In that first time trial, timers ran about 5-8 seconds after start, too short for live analysis. A slug decoded from the original 107-byte artifact was submitted after a retry and came back incorrect, because the retry had served a different 109-byte file.

Never submit an answer derived from a stale artifact: re-fetch and hash after every retry.
