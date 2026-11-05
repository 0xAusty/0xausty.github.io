+++
title = "Two of a Kind"
date = 2026-10-04
draft = true
params.kind = "challenge"
catalog_key = "day04-two-of-a-kind"
depth = "note"
featured = false
description = "A routine binary-to-text warmup, released on a day the Game Master returned 503 for hours and one session took the board from 25 to 48 of 62 modes."
solved_by = ["agent"]
tools = ["wusolve.py", "python"]
tags = ["encoding", "time-trial"]
skills = ["Automation & Tooling"]
toc = false
+++

Day 4 is binary, hinted by "only two sides", and it is routine. My notes hold nothing specific to this challenge beyond the day it landed on.

## The solve

The decode is eight-bit groups to bytes, then the slug. `wusolve.py` accepts that step only when the text is nothing but 0 and 1 and the length is a multiple of eight. The time trial and mastery were solved in the 4 October Claude Code session. Nothing records who submitted the single; the scoreboard puts it at 11:07:05 that morning, the time trial at 18:04:25 and the mastery at 18:06:19 that evening.

The day around it is the interesting part. On 4 October the Game Master returned 503 release_unavailable for hours from both endpoints, and that one session took the board from 25 to 48 of 62 modes.

A routine decode can be the least notable thing about its day.
