+++
title = "Metadata Forensics"
date = 2026-11-02
draft = true
layout = "lane"
lane = "metadata"
weight = 20

description = "A new file format almost every day and one precise field to pull from it, in a lane where the declared answer format decided how every value was spelled."

tags   = ["ctf", "forensics", "file-formats", "metadata", "pe", "elf", "evtx"]
skills = ["Digital Forensics"]
toc    = true
+++

Metadata Forensics brought a new file format almost every day and asked for one precise field from it. Over the month that meant ZIP structures and hashes; JPEG, PNG and PDF headers; PE headers, version resources and entry points; .NET metadata and its MVID; MSI databases; Windows shortcuts (.lnk); OOXML packages; email headers; WAV and MP4; ELF and Mach-O headers; APK and JAR manifests; SQLite; EVTX; registry hives; Windows Prefetch; pcap; GPT and MBR disk images; X.509 fingerprints; duplicate-content grouping; and, on the last day, an artifact graph.

Across the lane, the declared answer format decided the spelling, and the grader rejected the right value spelled any other way: hex padded to the field's full width, a CPU type as a `0x`-prefixed hex string where the architecture's name would seem the obvious choice, a GUID with braces and uppercase when it is stored as text but bare lowercase when it is binary, and an array sorted even where the field's syntax said "exact values and order".

`mfsolve.py`, one handler per day, carried the lane from Day 5 to Day 11. On 14 October Claude Code put `metaengine.py` in front of it, one pipeline from question to rendered answer; by 20 October it had 68 format parsers plus a guess-and-heal path for field names it had not seen before.

## What the lane kept asking for

From Day 3 every new question read "Determine <format>.<field> for <member>.": a parser, a field and a file inside the evidence zip. The answer format came in the start and submit responses, not the status call.

Day 1 set the habit: filename, size and three digests, each from the bytes of the named member. On Day 2 the answer id named a member inside the archive, and an AI analyst in the 2 October session read the outer ZIP's first 16 bytes instead. It was never submitted, but that day's time trials expired about 5 to 8 seconds after they started.

Day 8 turned the lane cumulative, and from Day 15, after five single-field days, the timed modes carried every earlier field again, up to 36 fields in the Day 31 time trial and 540 across its fifteen mastery sets, so every spelling rule followed into every later timed mode. The Day 2 prefix wanted lowercase hex with no `0x`; the Day 10 entry-point RVA wanted `0x` and the type's full width, so the minimal spelling was rejected. The MSI ProductCode is stored as text and went back verbatim, braces and uppercase; the .NET MVID is a binary GUID and went back canonical and lowercase. The width and the ProductCode spelling were learned from rejections; the lowercase MVID was accepted.

## How the solver took shape

**5 to 11 October, one handler a day.** `mfsolve.py` reached the repo on 5 October with the first daily runner, the morning the 09:05 sweep logged the Day 5 single as "NOT SUBMITTING (unmapped)". For a week the single was unsolved at release and the agent added the handler in session, from the PNG header on 5 October to a static VS_VERSIONINFO reader on 11 October. Who produced the Days 1 to 4 singles is not recorded; Days 12 and 13 were solved outside the repo, by whom and how not recorded.

**14 October, the engine.** The agent generalised the handlers into `metaengine.py`: parse the question, read the member through nested zips, run the matching parser, resolve the field by name, with or without its type tokens, and render from the answer format. It shipped with 37 parsers and answered every recorded field, 239 of 239. Most of its parsers covered formats nobody had asked for yet; EML, JAR, SQLite, EVTX, pcap, prefetch and X.509 each answered its single on the first submit.

**15 October, guessing from the parser.** The single had been unanswered at 09:00 on 10 of 11 days, Days 5 to 15, usually because a parser already held the value under another name, as on Day 15. I approved two things that day: `heal.py`, which banks the confident fields of a rejected submit, bisects the rest and tries format variants one field at a time, and closest-name guesses, which rank the parsed fields by word overlap with the requested name and submit the best as a suspect. Both submit only values parsed from the artifact.

**16 to 20 October, measuring generality.** On 16 October the agent built three novelty checks in the order I chose: a field-name leave-one-out, a differential check against independent readers, and wider format-token routing (68 to 115 of 117). Day 19 was the guess path's first live win, the ELF `e_machine` field CORRECT in all three modes by 09:00:13; the next morning's preflight showed the offline replay had silently lost the field, which had only ever scored through the live guess. Day 20's rejections became the representation fan in `guess_values`; `heal_audit.py` put unattended recovery on never-seen names at 77.5% before and 93.2% after.

**21 to 31 October, the remaining gaps.** Day 21 marked the limit: an APK is a ZIP, so the ZIP parser claimed it and the guess offered the member list as the package name; a manifest parser was written in session. Day 25 was the guess path as designed: a hive root name answered unattended, then exposed by the parser the same morning. Day 28 showed the fold-in-first loop: the single submitted from the session, the disk-image parser saved, and the supervisor's hot reload banking the timed modes within seconds. Day 31's `parse_graph` closed the month.

## Days worth knowing

- **Day 31 · [No Artifact Left Behind](/huntress-ctf-2026/day31-no-artifact-left-behind/)**: a provenance graph with a decoy loop, the greedy regex that turned the loop into a fake chain, and a morning of failed recovery paths.
- **Day 15 · [A Word to the Wise](/huntress-ctf-2026/day15-a-word-to-the-wise/)**: the document-order rejection, and the ranking model that made one miss worth more than any latency.
- **Day 19 · [Little Endian on the Prairie](/huntress-ctf-2026/day19-little-endian-on-the-prairie/)**: a perfect automatic day that hid a silent offline regression.
- **Day 11 · [What’s My Name Again?](/huntress-ctf-2026/day11-what-s-my-name-again/)**: a declared name against an on-disk name, and a one-shot retry saved by an offline test.
- **Day 14 · [The Shortcut Home](/huntress-ctf-2026/day14-the-shortcut-home/)**: a static .lnk parser, and the morning the handlers became one engine.
- **Day 20 · [Universal Appeal](/huntress-ctf-2026/day20-universal-appeal/)**: two spelling rejections that became a measured generality improvement the same day.
- **Day 21 · [Package Deal](/huntress-ctf-2026/day21-package-deal/)**: where self-healing stops; a re-spelling cannot fix a wrong fact.

## What the lane taught

- **The declared format decides the spelling.** Pad hex to the type's width, return a text GUID verbatim and a binary one canonical, and treat "exact order" with suspicion.
- **A live guess is a silent regression until it is folded in.** Day 19 proved it; Day 25 folded the guess in the same morning.
- **Self-healing recovers values the parser already holds.** A format with no parser is a miss however the guess is spelled, so coverage set the ceiling.
- **Pre-building parsers pays.** The 14 October parsers answered seven later singles on the first submit, six within a minute of release; the six singles that needed a parser written or extended in session were each CORRECT by 09:14.
