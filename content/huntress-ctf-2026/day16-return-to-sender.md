+++
title = "Return to Sender"
date = 2026-10-16
draft = false
params.kind = "challenge"
catalog_key = "day16-return-to-sender"
depth = "note"
featured = false
description = "The EML parser added two days earlier already exposed the Message-ID, so the pipeline solved the single and time trial at release; the mastery hit a lock."
solved_by = ["autopilot"]
tools = ["metaextra.py", "python"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

The single asked for the Message-ID of one message in a mailbox export full of replies, forwards, duplicates and reconstructed messages. The timed modes were cumulative bundles of 21 and 105 fields. For the pipeline it was a routine day.

## The solve

The EML parser added on 14 October (`metaextra.parse_eml`, built on Python's `email` package) already exposed the message ID. The release-time supervisor therefore answered the single and the time trial on its first submit, with no human fix. The raw header value was accepted, angle brackets included.

The mastery came back with an HTTP 409. It is locked until the time trial is correct, and the new parallel pipeline had started both together. The mastery was correct at 09:01:39, and the pipeline now runs single, then time trial, then mastery in sequence. The notes do not say who re-ran it.

The sequencing rule was already in the history: across 44 solved pairs, no mastery had been solved before its time trial.
