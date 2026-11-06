+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "Seven Steps"
date = 2026-10-14  # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day14-seven-steps"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 14 (2026-10-14), lane "warmups" (Warmups), web_no none
#   gm_id warmups-day-14
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "Ranking by decode steps let undecoded Atbash and Caesar chunks win and a fallback submit gibberish; the fix scored words mid-search and used the bundle as its own key."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = ["autopilot", "agent"]

tools  = ["python", "wusolve.py", "timed.py"]   # shown at the bottom + browsable
tags   = ["encoding", "classical-ciphers", "mastery"]
skills = ["Automation & Tooling"]  # groups it on /portfolio/

toc = true
+++

On Day 14 the pipeline submitted a wrong answer on its own. The decoder knew both of the day's slug ciphers, Atbash and a Caesar shift of 7, yet sent 68 mastery slugs, many ending in ciphertext: its ranking rewarded leaving a chunk undecoded, and the fallback added for Day 10 accepted the result. The fix scored words as they formed and, for the last three ties, used the bundle as its own key.

## The challenge

Each question, in all three modes, asked for the answer slug that a blob's final decoded line instructs you to submit: the slug alone, three lowercase words and two digits joined by hyphens, never the sentence around it.

The lane is cumulative. Day N's single is the whole sentence in Day N's new encoding, and the Day N mastery splits it into N chunks, chunk i in Day i's encoding. On Day 14 that put Day 13's Atbash and the new Caesar shift on the last two chunks, both inside the slug.

## Reading the prompt

One clue names both the cipher and the key.

| Phrase | Implication | What the solver did |
|---|---|---|
| "Caesar" | The new layer is a Caesar shift. | Nothing new: the decoder already tried all 25 shifts on every chunk. |
| "took a week off" | Seven days, so the shift is 7. | Nothing at release. From 11:02 that morning, `kpa.hint_steps` offers prompt numbers and number words ("week" is 7) as candidate keys, still validated by the search. |

The decoder could already undo both ciphers. It had no way to tell a decoded slug from an undecoded one.

## What was in the files

The single was the whole sentence under the day's Caesar shift; the time trial was a fresh blob. The mastery zip held 68 files of 14 numbered `NN<TAB>chunk` lines, each chunk encoded on its own, all on one schedule (in the solver's step names):

```text
01 base64      06 octal            11 base64
02 rot13       07 url              12 reverse
03 hex         08 html_entities    13 atbash
04 binary      09 unicode_escape   14 caesar7
05 decimal     10 base32
```

Decoded and joined, every blob reads the fixed 87-character sentence that the [first warmup](/huntress-ctf-2026/day01-a-little-based/) decoded to, then a slug from a closed vocabulary. The solver treats the sentence as known plaintext: a chunk's reading survives only if the text so far still matches it.

{{< callout type="warning" title="The known plaintext stops at character 87" >}}
The sentence check covers none of the slug. Past character 87 the search asked only for lowercase letters, digits and hyphens, and an Atbash or Caesar chunk left undecoded is exactly that.
{{< /callout >}}

## The solve

The supervisor saw the release at 09:00:02. The single and the time trial went through `solve_bytes`, which applies each step to the whole text and accepts a slug only after the decoded "Game Master:" phrase, so nothing comes out half-decoded. The 09:00:40 summary had both CORRECT, and the mastery not:

```text
[2026-10-14 09:00:40] 2026-10-14 day 14 (38s after release was seen)
  warmups-day-14: CORRECT
  warmups-day-14/time_trial: CORRECT
  warmups-day-14/mastery: incorrect
```

For many blobs the submitted slug began in plaintext and ended in Atbash or Caesar ciphertext. I was working with Claude Code in a local session that morning, and the agent traced the miss to two parts of `wusolve.py`.

The first was the ranking. `solve_lines` is a beam search: for each chunk it tries the chunk as it stands (`plain`), every decode step and every two-step chain, drops readings that break the known sentence, and keeps the 50 cheapest paths by decode-step count. `plain` costs nothing, and past the sentence an undecoded slug chunk passed the only check there was, as did every other shift of it. The readings that decoded nothing were therefore the cheapest, and the real one, two steps dearer, fell out of the beam.

The second was the fallback added for [Day 10](/huntress-ctf-2026/day10-thirty-two-below/), after a correct decode was rejected because "zesty" is missing from the laptop's word list. When no reading passes the dictionary, it accepts the strictly cheapest slug-shaped one. On Day 14 that was the undecoded reading.

The agent's fix, `6e23eb3`, committed at 09:32:44, changed the ranking. A new `_tail_unknowns` scores the slug as it forms: complete words must be dictionary words, the partial last word the start of one, and one unknown word is allowed so "zesty" still passes. Readings rank by unknown words, then decode steps. The fallback is gone; an exact tie gets no answer, or, in the words of the repo's hand-off notes, "ties are refused, not guessed".

```python
# before: the cheapest path per decoded text wins, and 'plain' costs nothing
c = sum(n.count('+') + 1 for n in p[1] if n != 'plain')

# after (6e23eb3): unknown slug words first, then decode steps
u = _tail_unknowns(cand[len(PREFIX):] if len(cand) > len(PREFIX) else '')
if u is None: continue
key = (u, cost(used + [n]))
```

Three blobs still had true ties, two shifts of the last chunk giving dictionary words at the same cost (Caesar-3 "step" against Caesar-7 "opal" in the notes' example), and the bundle settled them. `_bundle_schedule` returns the per-chunk path the resolved blobs share, only if at least three resolved and all agree, and the other 65 did. `timed.solve_artifact` then solves each tied blob again with that schedule, and a tied reading is accepted only if it alone follows it.

The mastery was CORRECT at 09:27:55. The fix, and the notes recording Days 12 to 14 at 15 of 15, were committed after that, at 09:32:44.

## Making it deterministic

The fix came with a regression test: `tests/test_wusolve.py` builds a Day-14-style blob (Base64 chunks for the sentence; reverse, Atbash and Caesar+7 for the slug), and the commit notes that it fails on the old search. Two smaller tests pin `_tail_unknowns` and the three-blob, all-agree schedule rule.

At 10:06 the agent added a replay corpus and a pre-commit gate: every recorded attempt is re-solved through the live code, and a changed or lost answer blocks the commit. The hand-off notes cite this Day 10 to Day 14 chain as their example. The gate only checks the past, but Day 14 is now part of that past, so letting undecoded chunks win again would fail it.

On 15 October the schedule became the fast path: one full search teaches the per-chunk path and the rest of the bundle decodes directly, accepted only as the exact sentence plus an all-dictionary slug, else back to the full search. Day 13 to 15 mastery solves fell from 2.4-4.4s to 0.06-0.09s.

## Timed modes

The time trial's deadline was 09:00:36 and the mastery's 09:00:38. The mastery was graded, and graded incorrect, so the clock was not what failed.

The fix still had to fit inside the clock, since warmups mastery windows had run roughly 7 to 13 seconds on Days 10 and 11. `6e23eb3` also hoisted `_chunk_cands` out of the per-path loop, decoding each chunk once instead of once per beam path: 0.28s to 0.094s a blob, 4.3s for all 68.

On 28 October, in a broad pass on the speed boards, a ranked Day 14 time trial and mastery both came back CORRECT, with board times the log estimated at about 1.12-2.41s and 1.25-2.46s.

## Dead ends

- **Fewest decode steps as the ranking.** It rewards doing nothing, since `plain` costs zero. Replaced by unknown words first, steps second.
- **The Day 10 cheapest-shape fallback.** It rescued one missing word on Day 10; on Day 14 it accepted garbled slugs for many of the 68 blobs and produced the incorrect submit. Removed; the one-unknown-word allowance covers its case.
- **Solving Day 13 outside the solver.** The day before, the [Day 13](/huntress-ctf-2026/day13-opposite-day/) mastery's release run showed the same symptom (slug words still reversed or Atbash-encoded), and with no answer for 11 of the 63 blobs the runner, which submits only when every answer is solved, held back. That mastery was solved outside the repo, by a route the notes do not record, with no solver change committed, so the solver went into Day 14 unchanged.

## Takeaways

1. **Rank by evidence before cost.** Whether the words exist is the evidence; step count should only separate readings that both have it.
2. **Shape is not validity.** Atbash and Caesar map letters to letters, so a character-class check passes ciphertext as readily as plaintext.
3. **A fallback is a guess with a cost function.** The Day 10 rule rescued one real word and, four days later, submitted gibberish. Its replacement allows one unknown word and refuses ties: the never-guess rule I set for the pipeline, applied inside the solver.
4. **Ask the rest of the bundle.** Sixty-five blobs agreed on one schedule, and that settled the three that could not settle themselves.
