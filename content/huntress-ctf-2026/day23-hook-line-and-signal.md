+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Hook Line and Signal"
date = 2026-10-23  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day23-hook-line-and-signal"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 23 (2026-10-23), lane "mobile" (Mobile (Android)), web_no none
#   gm_id mobile-android-day-23-hook-line-and-signal
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = true                    # true → appears in the hub's "Start here"

description = "The answer code stopped sitting in a JSON asset and was computed in Dalvik bytecode, so Claude Code wrote a DEX parser, a Dalvik interpreter and an x86-64 JNI interpreter."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["mobsolve.py", "mobemu.py", "dexdis.py", "nativemix.py", "objdump", "python"]
tags   = ["android", "dex", "jni", "emulation", "mastery"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = true
+++

Day 23 is where the mobile lane's working assumption broke. For 22 days the APKs had carried their answer code in `assets/huntress_puzzle.json`, under a new encoding each day, and static decoding had been enough. On Day 23 that file held only metadata, and the code was computed by the app's own bytecode. My laptop had no jadx or baksmali, so in a recovery session Claude Code wrote the tools itself: a DEX parser, a small Dalvik interpreter and an x86-64 interpreter for the JNI side. The analysis and the code below are the agent's.

## The challenge

Every question asked for one field, `answer` (one per set in the mastery). Each named a case reference and the app's package, repeated the prompt and ended "Submit only the exact backend answer code returned for this case." The answer is the lane's usual code: the `ANS` prefix, a hyphen and 16 uppercase hex digits, matched exactly.

The mastery's seven APKs each re-implemented one day's mechanism: Days 2, 6, 10, 14, 15, 22 and 23. The Game Master opens the modes in order: single, time trial, mastery.

## Reading the prompt

The prompt is one sentence; the question wrapped around it adds a third clue.

| Phrase | Implication | What the solver did |
|---|---|---|
| "real instrumentation signals" | The answer comes from the chain that `Release.code()` actually calls. | `mobemu.py` runs `Release.code()` and follows each call as it is made. |
| "generated false positives" | Generated decoy methods sit beside the real ones, and nothing calls them. | Nothing to filter: an interpreter only reaches what the chain invokes. |
| "the exact backend answer code returned for this case" | One code per case, exact match; computed this time, not stored. | Keeps only a result that starts with the `ANS` prefix; the mastery submit paired each set with its APK by package and file name. |

The agent's note says it in one line: follow the actual call chain, because "uncalled decoy methods are the false positives".

## What was in the files

The puzzle file was a new version with metadata and nothing else: codec `analysis`, no data. The answer lived in `classes.dex`:

```text
assets/huntress_puzzle.json   metadata only: codec "analysis", no data
classes.dex
  Release.code()              the ANS prefix and "%016X" formatted over finalMix(token())
  token(), f1, finSignal, …   pure 64-bit long mixers: XOR, add, multiply by an odd constant, rotate
  decoy methods               generated, never called
lib/x86_64/libarena.so        in the Day 15 mastery APK: JNI function nativeShare, a pure x86-64 mix
```

The mixers are pure functions of 64-bit values, so running them needs almost nothing of Android. The exception was the APK that re-ran [Native Library Secrets](/huntress-ctf-2026/day15-native-library-secrets/): its chain calls `nativeShare`, a native method with no bytecode, whose x86-64 body in the bundled library is also pure arithmetic.

## The solve

The supervisor saw the release at 09:00:02. On its first pass the static solver, `mobsolve.py`, still answered the single, and the answer was accepted; my notes don't record which of its paths found it. For the time trial it came back empty, `sol {None: None}` and then `NOT COMPLETE (unmapped)`, so nothing was submitted, and the mastery, locked behind it, never started. The pass closed at 09:02:14 with 10 of the day's 24 modes banked and this for mobile:

```text
  mobile-android-day-23-hook-line-and-signal: CORRECT
  mobile-android-day-23-hook-line-and-signal/time_trial: unsolved
  mobile-android-day-23-hook-line-and-signal/mastery: not attempted
```

An earlier agent session then cleared the time trial, the warmups mastery and all three web challenges, and died; the notes don't say how it got the time trial. A fresh local session picked up what was left: this mastery at 0 of 7, and the time trial of the script lane's [Press Start to Decode](/huntress-ctf-2026/day23-press-start-to-decode/) at 0 of 1,495.

With `objdump` on the laptop but no DEX tooling, the agent wrote three tools:

- **`dexdis.py`**, a minimal DEX parser and Dalvik disassembler. It reads the header's ID tables and each class's methods, and prints the app's code as Dalvik mnemonics.
- **`mobemu.py`**, in its own docstring a "Tiny Dalvik emulator". It wraps `long` and `int` arithmetic the way Java does, handles arrays, static fields and branches, recurses into the app's own static methods, and stubs the few framework calls its docstring names: `StringBuilder`, `String.charAt`, `Long.toHexString`. An unknown opcode raises `NotImplementedError`. Its `solve_apk` calls each method named `code` and keeps a result only if it starts with the `ANS` prefix.
- **`nativemix.py`**, for the native step. It disassembles the bundled library with `objdump` and interprets the named `Java_` function top to bottom: `mov`, `add`, `xor`, `imul`, `rol`, `ror`, the shifts and a few more; anything it doesn't model raises. JNI puts the `JNIEnv` pointer and the calling class or object in `rdi` and `rsi`, so the `jlong` argument arrives in `rdx`, and the result is `rax` at `ret`. `mobemu.py` registers each `Java_` function under its Java method name, so `nativeShare` is called like any other method.

A small script in the session's scratchpad, `mobmaster.py`, reconnected to the mastery attempt, matched each set's question to its APK by package and file name, and submitted all seven codes, which were accepted. The card has no time for the last two modes; the server's final challenge list has the time trial solved at 09:22:31 and the mastery at 09:58:28.

## Making it deterministic

The session left the three tools untracked in `solvers/`, wired into neither `mobsolve.py` nor the replay gate, with a note from the agent to itself: make the emulator the path for puzzle files with no data, and add a mobile replay test.

The wiring landed the next morning, 24 October, at 10:02:59 in `d0624a1`: `mobsolve.py` now hands any APK whose puzzle file declares the `analysis` codec to `mobemu.solve_apk` before trying to decode the file. The comment on that branch names a second kind of decoy, `ANS` literals elsewhere in the package. They make the solver's old last resort, a scan that accepts a code only when exactly one appears, ambiguous, so the emulator runs first.

That was a release late. `d0624a1` is the Day 24 fold-in, and its message lists this wiring among the fixes for five Day 24 shapes that no solver had handled at that morning's sweep ([Emulator Alibi](/huntress-ctf-2026/day24-emulator-alibi/) is that day, and its sweep went like Day 23's: single banked, time trial empty). The emulator was on disk; the pipeline didn't call it.

The commit also left out `nativemix.py`, a gap the agent's note flagged: a fresh clone, or the next mobile challenge with a native library, would break. It followed at 10:08:30 in `e21f6fe`, imported only when an APK bundles a `.so`. `mobemu.py` kept growing in the Day 25, 26 and 31 fold-ins, and `nativemix.py`, written for strictly linear code, gained compares and conditional jumps on Day 25.

## Timed modes

Neither mode had a clock in regular play: the log shows `deadline None` for the time trial, and the Game Master's guidance for both said a correct untimed solve still earns the flag and the points. Only the ranked Hall of Fame versions were timed, at 50 s and 230 s.

What mattered was the order. The pipeline runs a lane's time trial only after its single, and its mastery only after its time trial, because the Game Master refuses them otherwise; one time-trial miss cost the mastery its morning run. Finishing at 09:58 rather than 09:02 cost no points, but on a scoreboard that breaks ties by who reached the score first, it cost time. The mastery's seven mechanisms, one of them native, needed no per-day code: the emulator ran whatever `Release.code()` did.

## Dead ends

- **Static decoding.** It had worked for 22 days; on the time trial it found nothing to decode, and the pipeline, which submits only when every answer id has an answer, moved on.
- **The first recovery session.** It got the time trial through and then died, and the rest of the work moved to a fresh local session.
- **A mastery attempt at 09:40:41.** The attempt records mark it unsolved, ahead of the emulator-based submit at 09:58:28.

## Takeaways

1. **When the answer moves into code, run the code.** The puzzle file stopped carrying the answer, so the agent stopped decoding and interpreted `Release.code()` instead.
2. **Execution sorts signal from decoys.** An interpreter never runs an uncalled method, so the false positives drop out without a filter.
3. **Model what the target uses, and fail loudly on the rest.** Both interpreters raise on an instruction they don't know, and later fold-ins extended them as new shapes arrived.
4. **A tool isn't finished until the pipeline calls it.** The emulator solved the mastery on 23 October, sat untracked overnight, and the Day 24 sweep ran without it.
