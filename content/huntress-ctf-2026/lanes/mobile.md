+++
title = "Mobile (Android)"
date = 2026-11-02
draft = true
layout = "lane"
lane = "mobile"
weight = 50

description = "Static APK analysis without a device: a new codec in a JSON asset each day, then codes computed in the DEX and recovered with a Python Dalvik interpreter."

tags   = ["ctf", "android", "apk", "dex", "jni", "emulation", "reverse-engineering"]
skills = ["Reverse Engineering"]
toc    = true
+++

The mobile lane was static APK analysis without a device. For the first 22 days the answer sat in one asset, `assets/huntress_puzzle.json`, under a codec that changed by day: plain, reversed, Base64, XOR and split-and-reorder on Days 1 to 5, `indexed` on Day 17, and a breadth-first search over decode chains for anything unnamed.

From Day 23 that asset could hold only metadata, with the code computed in `classes.dex` through chains of 64-bit mixing functions and, in one of that day's mastery sets, a native x86-64 function. That called for a DEX parser, a small Dalvik interpreter (`mobemu.py`) and an x86-64 interpreter for the JNI side (`nativemix.py`), all written by Claude Code in a session that day. The same tooling then met Java reflection, split App Bundles and a second DEX loaded at runtime.

Whatever the prompts said about anti-debug and root checks, no solve on record ran on a device or in an Android emulator: the puzzle file was decoded as data, and from Day 23 the bytecode was interpreted in Python.

## What the lane kept asking for

Every mode asked the same one-field question: a case reference, the app's package, an attack story and a request for the backend answer code for that case. The field was `answer`, matched exactly: a fixed four-character prefix and 16 uppercase hex digits. The solver returned nothing that failed the same regex.

The code was always in the package: one APK for the single, a fresh one for the time trial, one per `setN.answer` for the mastery, which held three or five APKs until Day 21 and then grew by one a day from Day 22's six to Day 31's fifteen, the later ones re-implementing earlier days' mechanisms.

The clock moved under the lane: deadlines about 5 to 8 s after start on Day 2, none on Days 8 and 9, re-armed on Day 10, untimed in regular play from Day 15 unless a ranked attempt was requested.

## How the solver took shape

**2 to 5 October.** The first harness started all five Day 2 time trials before any analysis was ready; all five expired. A 4 October session, credited to the agent, cleared every open mobile time trial and mastery; `mobsolve.py` followed on 5 October at 11:19, with branches for the first five codecs, `hex` and `rot13`, and a generic search over decode chains for anything unnamed, beside a generic timed runner that goes from start to submit in about 1.5 to 3 s. That morning's run had been one codec short: Day 5 dropped before 09:00, and when the runner saw it at 09:05:15 the solver returned nothing for the new split-and-reorder puzzle and declined to submit. The split branch tries both readings of `order` and accepts only a unique valid code; all three modes were CORRECT at 09:06:51, 09:06:53 and 09:06:55, submitter unrecorded.

**6 to 22 October.** From Day 6 the cron runner banked the lane at release on most mornings, about a second per mode. The exceptions: Day 8, run in session after the laptop slept through the cron; Day 9, banked by 09:02:10 after the 08:50 cron chased a stale marker and quit; Day 16, a mastery 409 for starting it alongside the time trial, re-run in session; Day 17, a miss on the new `indexed` codec. On 14 October the replay gate caught what no live run had: a new digit-rotation step in the warmups solver, whose steps `generic_decode` reuses, made the Day 7 and Day 14 codes ambiguous with a second, deeper well-formed code. The fix lets the shallowest depth decide.

**23 to 26 October.** Day 23's time trial carried the `analysis` codec with no data: static decoding returned nothing and the mastery stayed locked. The time trial was CORRECT at 09:22:32 from a session that then died; a fresh session wrote the three tools and had the seven-set mastery CORRECT at 09:58:29; the next morning the emulator was wired into `mobsolve.py`. On 25 October the supervisor's new hot reload made fixing a loop: each saved emulator fix reopened the 7/9 mastery within seconds, and the tenth reload at 09:24:54 came back CORRECT. On 26 October the single and time trial were split App Bundles whose answer exists only once base and feature splits are merged; the fix landed in session, the reload banked the time trial and mastery by 09:21:50, and that afternoon the emulator became the fallback whenever static decoding failed on a `classes.dex` APK.

**27 to 31 October.** Day 27's eleven-set mastery banked unattended 12.1 s after release. Then three new single codecs on three mornings, each a miss at 09:00. Day 28's `packet`, a hex frame with the code in frame order: recovery waited about 11 minutes for someone to notice; the supervisor's hot reload then banked the time trial and mastery by 09:15:37. Day 29's `table`, a per-position affine key that the answer format's known prefix pins: only the single needed it, and the supervisor then banked the other two modes itself by 09:11:09. Day 30's `layered`, composed layers over a declared key, peeled breadth-first with ambiguity refused: fixed by an agent the supervisor launched itself, all three modes by 09:05:06. Day 31's fifteen-set gauntlet solved 14 of 15 at release; the one failure, a Day 20-style app, needed the emulator to load a second DEX at runtime, added inline.

## Days worth knowing

- **Day 23 · [Hook Line and Signal](/huntress-ctf-2026/day23-hook-line-and-signal/)**: the full write-up: static decoding stopped working and the agent built its own DEX tooling.
- **Day 16 · [JNI Boundary](/huntress-ctf-2026/day16-jni-boundary/)**: a parallel shortcut refused with a 409, and #1 on the speed board at 0.409 s until a 0.407.
- **Day 17 · [Name Collapse](/huntress-ctf-2026/day17-name-collapse/)**: the `indexed` codec, a one-minute fix that waited twelve, and the triage rule it produced.
- **Day 25 · [Integrity Signals](/huntress-ctf-2026/day25-integrity-signals/)**: ten hot reloads, reflection support and a branching x86-64 interpreter.
- **Day 26 · [Split Decision](/huntress-ctf-2026/day26-split-decision/)**: the answer split across App Bundle splits the solver had treated as separate apps.
- **Day 29 · [White Box Key Recovery](/huntress-ctf-2026/day29-white-box-key-recovery/)**: four known bytes of the answer format recover an affine per-position key.
- **Day 30 · [Layered Protections](/huntress-ctf-2026/day30-layered-protections/)**: a breadth-first peel that refuses ambiguity, fixed by an agent nobody launched by hand.
- **Day 31 · [Mobile Arena Gauntlet](/huntress-ctf-2026/day31-mobile-arena-gauntlet/)**: fifteen apps built from earlier mechanisms, fourteen solved unattended, one runtime-loaded DEX.

## What the lane taught

- **Read the format line, not the attack story.** Every prompt described a runtime exploit; every answer was data or a computation inside the package.
- **Refuse ambiguity instead of guessing.** Two readings of `order`, a rotated code that is also valid, decoy literals: the decoder returns nothing unless exactly one candidate survives.
- **A miss early in the chain cascades.** Each mode is locked until the one before it is CORRECT, so a new shape on the single held up the two modes behind it.
- **Shared code needs a shared gate.** A warmups change can break mobile, and the replay corpus caught one before it cost a live answer.
- **Build the tool you lack.** No jadx, no baksmali, objdump present: a DEX parser, a Dalvik interpreter and an x86-64 interpreter written in a session carried the lane to the end.
