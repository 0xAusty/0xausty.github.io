+++
title = "Hear Me Out"
date = 2026-10-17
draft = true
params.kind = "challenge"
catalog_key = "day17-hear-me-out"
depth = "note"
featured = false
description = "The grader wanted ffprobe's codec name, which qualifies PCM by sample format, so the media parser sniffs the container and reports ffprobe's vocabulary."
solved_by = ["agent"]
tools = ["metaformats.py", "python"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

The single asked for the primary audio codec name of a voice note that had been transcoded, renamed and embedded in mail. The timed modes were cumulative bundles of 22 and 110 fields. The twist was whose vocabulary the grader used.

## The solve

The pipeline's closest-name guess returned the WAV format tag's generic PCM name, and the self-healing re-spelling in uppercase was rejected too, both at 09:00. The grader wanted ffprobe's `codec_name`, which qualifies PCM by sample format and endianness.

Claude Code added `metaformats.parse_media` in session. It sniffs the real container from the bytes, whatever the extension claims, and reports ffprobe's names on top of the container fields. It covers WAV and RF64, Ogg, FLAC, MP4, Matroska, AIFF, AU, AMR, CAF, ASF and MPEG audio, and it was committed with tests.

The single was correct at 09:01:38, the time trial at 09:04:52 and the mastery at 09:04:59. Four lanes changed their questions that day, and the day's finish came from the binary lane, not this one.

When a grader quotes a tool's output, answer in that tool's vocabulary.
