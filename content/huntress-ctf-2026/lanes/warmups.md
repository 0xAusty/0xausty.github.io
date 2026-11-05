+++
title = "Warmups"
date = 2026-11-02
draft = true
layout = "lane"
lane = "warmups"
weight = 10

description = "One blob a day in a new encoding, Base64 to Brainfuck, and masteries that split one known sentence across all of them, solved by checking every decode against known plaintext."

tags   = ["ctf", "encodings", "classical-ciphers", "automation"]
skills = ["Automation & Tooling"]
toc    = true
+++

The warmup lane handed out one blob a day, each in a new classic encoding. Over the month that meant Base64, ROT13, hex, binary, decimal, octal, URL percent-encoding, HTML entities, backslash escapes, Base32, URL-safe Base64, string reversal, Atbash, a Caesar shift of seven, ROT47, hex spelled in Morse, hex-nibble Bacon groups, a three-rail rail fence, UTF-16 in either byte order under hex, gzip under Base64, Ascii85, comma-joined count:char tokens, Unicode code points, Brainfuck and its Ook! dialect, and in the last four days combinations of earlier ones, ending with Base64 over gzip over Base32. A few of those come from the day's prompt, not my notes.

The masteries were the cumulative part. Day N's mastery was a bundle of 5N−2 blobs, three on Day 1 and 153 on Day 31. Every blob split the same sentence into N numbered chunks, chunk i in Day i's encoding, so the day's new encoding always landed on the slug: three lowercase words and two digits. At that volume a decoder can't stop as soon as its output looks decoded.

So `wusolve.py`, the lane's solver, which Claude Code wrote in sessions I steered, checks every decode against the instruction sentence the blob is known to contain and against a dictionary for the slug words. When a layer needs a key, `kpa.py` recovers it from that known plaintext.

## What the lane kept asking for

Every question, in every mode, asked for the slug that the blob's final decoded line tells you to submit, and only the slug. That cost one wrong submit on Day 3, when a generic decoder in the first harness sent the whole sentence. The cure was a slug extractor keyed on the fixed phrase before the slug, and it also let the timed modes run unattended.

Every blob decoded to the same fixed 87-character instruction followed by the slug, and the slug words came from a closed vocabulary: 48 per slot, 142 distinct, nothing new after Day 9. With known plaintext and a closed word list, decoding became checking, and later key recovery.

The clocks moved. On 2 October the time-trial timers expired about 5 to 8 s after start, Days 8 and 9 had no deadline, Day 10 re-armed the mastery at about 10 to 13 s and Day 11 at about 7 to 10 s. On 15 October the Game Master's API description showed that regular play is untimed by default and a ranked speed-board attempt has to ask for `run_for_time`, which the runners had never done. Each mode also stayed locked until the one before it was correct, so one missed single cost all three.

## How the solver took shape

**2 to 6 October.** The agent's first harness decoded Base64, hex and prompt-gated ROT13 and returned the whole decoded text. Day 2's time trial showed that a retry can serve a different artifact without saying so. The agent then wrote `wusolve.py` and `timed.py`: a bounded breadth-first decode that stops when the instruction appears with three dictionary words, a chunk-by-chunk mastery solver that keeps only readings consistent with the known prefix, and a one-process fetch-solve-submit runner of about 2 s. The cron runner, installed at my request, was five minutes late on its first morning because Day 5 came out before 9:00.

**8 to 11 October.** The scheduling broke first. Cron skipped the job the laptop slept through, then a stale day marker sent the next run back to Day 8; the fix was a self-healing marker and a persistent systemd timer. On Day 10 the bug was the dictionary: a correct decode was rejected because "zesty" is not in the system word list, so the agent added a fallback to the cheapest reading, accepted only when unique. On Day 11 the answer was right and still lost. A serial 53-blob solve took about 18 s against a 7 to 10 s window, and a forked process pool and trimmed hot loops brought the round trip down to about 4 s.

**14 to 16 October.** The Day 10 fallback accepted gibberish on Day 14 and the pipeline submitted a wrong mastery on its own. The fix scored slug words against the dictionary as they formed and refused ties; three genuine ties were settled by the schedule the other 65 blobs agreed on. The same morning brought the replay corpus, a pre-commit regression gate and `kpa.py`, known-plaintext key recovery. On 16 October a 400-wide search frontier dropped Morse's hex child. `wufuzz.py` then fuzzed every encoder pair and sampled triples, and found 16 more unreachable pairs, fixed the same morning.

**17 to 25 October.** New shapes kept arriving, and each fix was in the solver before the time trial and mastery ran: hex-nibble Bacon (Day 17), a UTF-16 detector (Day 19), a combined Base64-plus-decompress step (Day 21), run-length tokens (Day 24), code points (Day 25). Day 18's rail fence needed none, because `kpa.py` keyed it from the known sentence. On 19 October the gate blocked a correct fold-in twice and exposed two latent faults. From 25 October hot reload re-solved and submitted the open modes within about 10 to 30 s of a save.

**26 to 31 October.** After the Day 26 retro I reset the plan: speed comes from pre-covering each lane's bounded set of shapes, not from infrastructure. That afternoon the agent added Ook! ahead of release, and Day 27 banked in about 16 s. Day 31's three-layer blob found one more gap, a combined step missing from the fast search's first steps.

## Days worth knowing

- **Day 14 · [Seven Steps](/huntress-ctf-2026/day14-seven-steps/)**: the pipeline's own wrong submit, traced to the previous fix and repaired with the bundle as its own key.
- **Day 11 · [Safe Travels](/huntress-ctf-2026/day11-safe-travels/)**: every blob decoded correctly and the 9:00 mastery still scored nothing, because the solve ran longer than the window.
- **Day 16 · [Dot Com](/huntress-ctf-2026/day16-dot-com/)**: hex in Morse fell past a 400-wide frontier, and the fuzzer it prompted found 16 more.
- **Day 19 · [Little Things](/huntress-ctf-2026/day19-little-things/)**: a correct live fix that the regression gate refused twice, rightly.
- **Day 25 · [You Have a Point](/huntress-ctf-2026/day25-you-have-a-point/)**: hot reload turned "fix the solver" into "save the file"; the time trial and mastery banked two seconds apart.
- **Day 27 · [Monkey Business](/huntress-ctf-2026/day27-monkey-business/)**: Ook! added the afternoon before as proactive coverage; all three modes banked by 09:00:18.
- **Day 31 · [One More Thing](/huntress-ctf-2026/day31-one-more-thing/)**: one missing first step turned a sub-second decode into a wedged worker that froze the supervisor.

## What the lane taught

- **Validate against what you know.** Known plaintext and a closed vocabulary turned decoding into checking. A slug-shaped reading proves nothing when the cipher is a letter substitution.
- **On a timed mode, throughput is part of correctness.** A right answer after the deadline scores nothing, and a search's width and order decide what is reachable.
- **A fix can be the next bug.** Day 10's fallback produced Day 14's wrong submit. A replay gate over every past case, caches cleared, catches that before the next release.
- **Pre-cover the bounded universe.** The lane's encodings were a finite set, and the one added the afternoon before it arrived is why Day 27 needed nobody.
