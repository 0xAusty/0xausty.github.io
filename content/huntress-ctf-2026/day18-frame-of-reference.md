+++
title = "Frame of Reference"
date = 2026-10-18
draft = true
params.kind = "challenge"
catalog_key = "day18-frame-of-reference"
depth = "note"
featured = false
description = "The accepted video geometry was the coded size from the MP4 sample entry as WxH, not the display size, rotation or aspect ratio."
solved_by = ["agent"]
tools = ["metaformats.py", "python"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

The single asked for the primary video dimensions of an MP4 as WxH, hidden among clips, previews, crops and screen recordings. The timed modes were cumulative bundles of 23 and 115 fields. It was a quick day, and metadata needed only one field, so it was fixed first.

## The solve

The media parser from the day before knew only audio streams. The closest-name guess therefore returned the video codec's name, and the uppercase re-spelling was rejected too, so the single stood as incorrect at 09:00:44.

Claude Code extended `parse_media` for video. For MP4 it reads the track header's display size and rotation matrix, the visual sample entry's coded size, the pixel aspect box, the AVC profile and level, and the frame rate and count from the sample tables. For Matroska it reads the pixel and display dimensions. The accepted `primary_video_dimensions` is the coded size from the sample entry.

The single was correct before the time trial at 09:02:20; its exact time isn't recorded. The mastery followed at 09:02:27 and the day was complete by 09:03:46.

Coded size, display size and rotation are different fields, and the grader asked for the first.
