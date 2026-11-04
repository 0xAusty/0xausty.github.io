+++
title = "A Word to the Wise"
date = 2026-10-15
draft = true
params.kind = "challenge"
catalog_key = "day15-a-word-to-the-wise"
depth = "note"
featured = false
description = "External relationship targets had to be sorted, not in document order, and the same day taught the lane that text GUIDs are answered verbatim."
solved_by = ["agent"]
tools = ["msimeta.py", "mfsolve.py", "metaengine.py", "python"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

The single asked for the external relationship targets of a Word document as a compact JSON array. The timed modes were cumulative: 20 fields in the time trial, 100 in the mastery, covering every earlier day's field plus a new question asking for the named files in ascending SHA-256 order.

## The solve

The 09:00 run left the single unanswered, because the parser already held the list under another name. The first answer, in document order, was rejected at 09:01, and the array has to be sorted. The first time-trial submit at 09:05 was rejected on five fields carried over from Days 4 to 7; the notes do not say which fix cleared them.

Claude Code fixed the rest in session and committed it. It added the digest-order question, answered the MSI product code verbatim (braces, uppercase) while the binary .NET module ID stayed lowercase, and followed the mastery's first hop into the per-set inner zip, since the sets repeat member names. The mastery was correct by 09:07:22 and the whole day, all 15 modes across the five lanes, was complete by 09:18:56.

The day also showed that a miss costs more than slow solving: 86 teams were tied on points, and the tie-break was the time a team reached its score.
