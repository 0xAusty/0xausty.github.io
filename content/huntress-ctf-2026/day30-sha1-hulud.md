+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "SHA1-Hulud"
date = 2026-10-30  # the challenge's release date (today's date when the file name is not a catalog key)
draft = false                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "day30-sha1-hulud"
# From the catalog (read-only; the templates pull these from data/huntress_ctf_2026.json):
#   day 30 (2026-10-30), lane "binary" (Binary Reverse Engineering), web_no none
#   gm_id binary-reverse-engineering-day-30-sha1-hulud
depth = "full"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "The month's one miss: a stripped Rust PE emulated offline in Unicorn, where a confident one-way verdict was overturned and a loader bug kept the cipher gate shut."

# Who got it, most important first: autopilot | agent | homebase | chatgpt
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
#   chatgpt   → "ChatGPT, on my own account, supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = []   # unsolved in the catalog: no label applies

tools  = ["python", "unicorn", "capstone", "gcc"]   # shown at the bottom + browsable
tags   = ["reverse-engineering", "pe", "rust", "emulation", "obfuscation"]
skills = ["Reverse Engineering"]  # groups it on /portfolio/

toc = true
+++

SHA1-Hulud, a standalone reverse-engineering single on Day 30, is the one miss of my month: 560 of 561 modes went CORRECT, and this was the 561st. My own ChatGPT account, two Claude Code takeovers and the event's Homebase AI (GPT-6 Luna) were all put on it, and none produced a flag. What went wrong is worth the space: a confident "one-way" verdict that was wrong, two sessions reading the same code two ways, and an emulator bug behind a long detour.

## The challenge

The binary lane's daily challenges hid the same XOR'd, CRC32-checked configuration record somewhere new each day. SHA1-Hulud was a traditional CTF reverse-engineering task instead: one untimed single-solve mode with one answer field, `flag`. According to the event Discord, every team got a different binary and flag, so there was no shared answer to look up or guess.

## Reading the prompt

The prompt, on the card above, is mostly theme. The agent's notes tie the title to the Shai-Hulud npm supply-chain worm and take "SHA1" literally, which the binary bore out.

On 31 October I relayed the challenge author's hint from Discord: "hopefully by doing it by hand you understand the challenge prompt I gave." The notes took it to mean reading the code rather than automating it.

## What was in the files

The zip held `sha1-hulud.exe`, a stripped PE32+ x86-64 console program of 632,320 bytes, built in Rust with `embre`, the challenge author's own crate. What the sessions had mapped by the end:

- **Strings.** `embre` stores each string as an XOR pair, bytes then key, and checks input against it without decrypting. There are six (`ProgramFiles`, the prompt, the success text and three DLL names); none is the flag.
- **Protected functions.** Four large functions each open with an `int3` that the program's own vectored exception handler catches, poisoning the keys under a debugger. All four are SHA-1's 80-round compression without the final feed-forward: one standard, one whose message schedule taps word 9 where SHA-1 taps word 8, one rotating `b` by 2 instead of 30, and one whose variant was never identified.
- **Before the prompt.** It hashes its own `.text`, 8,040 blocks, with three of those functions and runs two pointer-chasing "time-lock" loops of tens of millions of iterations.
- **Anti-analysis.** APIs resolved by name hash, a CPUID hypervisor-bit check, RDTSC timing probes at 16 sites, firmware-table and `KUSER_SHARED_DATA` reads, and an LZNT1-compressed blob unpacked at run time.
- **A gate.** The cipher stage runs only if a 16-entry byte table, expanded from an 8-byte seed, holds a repeated non-zero value. Otherwise the program exits silently.

Past the gate, as the second takeover read it:

```text
input -> lower-cased -> "flag{" + input + "}"
      -> u64 length || bytes, zero-padded to a multiple of 16
      -> pass 1: CBC-like chain; 16-round permutation keyed from a running SHA digest
      -> pass 2: backward chain; 16-round permutation, constant key
      -> bytewise masked compare against expected bytes generated at run time
```

Both passes invert: every round step (key material added or XOR'd in, a Klimov-Shamir T-function, x + (x² OR 5), rotations, xorshifts) can be undone, and pass 1's key for a block depends only on earlier plaintext.

## The attempt

I left for a camping trip on the morning of 30 October and spent the 31st in the Appalachian Mountains on campground wifi, so I had far less time at the laptop, and a far worse connection, than during the rest of the month. The laptop had no Ghidra, IDA, angr or Wine, so the work was mostly offline emulation.

**30 October.** The pipeline's supervisor logged `resolved 0 / 1` on every pass that morning. The escalator, a headless Claude Code run started on first-pass misses, took it up at 09:00:31 and died at 09:07:26:

```text
[2026-10-30 09:07:26 EDT] claude escalator exited non-zero
You've hit your session limit · resets 1:30pm (America/New_York)
```

With my Claude usage limit hit, I took the binary to my own ChatGPT account. That session built an offline Unicorn emulator, `emu_clean.py`, and an inverse of the input transform, and captured seven "candidates" at a compare site. None decoded.

**The first takeover.** That night the agent took the emulator over and fixed its two blockers: an unknown ntdll API hash, brute-forced to `NtQueryVirtualMemory`, and the CPU probes, which needed deterministic CPUID and RDTSC hooks before the captured data stopped changing. It showed the ChatGPT inverse was correct and useless: applied to the transformed input, it only ever gave back what was typed. It read the capture site as a SwissTable hash-map probe (Rust's hashbrown), which made the candidates noise. Its handoff, written by about 23:15, set a rule: "Do not submit a guessed flag; submit only a value verified against the binary's own check."

**31 October: the one-way detour.** The notes for this day overlap, so the order is approximate. A reboot that morning wiped the first emulator and its memory dumps from `/tmp`. The agent's sessions ported the inverse to C and scanned the exe, the unpacked blob and heap dumps from three points in the run for the flag in raw, transformed and XOR'd forms, down to the XOR of any two of 541 referenced data arrays. Only the player's own input turned up. The verdict: a one-way digest, so nothing in the binary could give the flag back.

The notes also record AI sessions tripping a safety classifier on the worm-themed binary. At 09:01:38 the escalator launched five agents, one on SHA1-Hulud; all five were killed at a 600-second ceiling (the Day 31 notes name the setting that lifts it). Those notes then left SHA1-Hulud to me "on purpose". I put it to the Homebase AI; the notes record no result.

**The second takeover.** A later session rebuilt the harness in four stages, `emu.py` to `emu4.py`, ending with native ports of three SHA-1 variants and both time-lock loops, each checked against emulation. It decoded both cipher passes and wrote their inverses in `cipher.py`, round-trip tested. It read the capture address, `0x140059cd9`, as the final masked compare with expected bytes generated at run time: nothing stored to find, and a cipher that runs backwards. Its note says the one-way note's "inference was wrong".

After a long detour it also found why the gate stayed shut and the cipher never ran: the binary hashes its `.text` up to `SizeOfRawData`, but the harness's PE loader zero-filled the 138 raw bytes past `VirtualSize`, which changed the hash and the keys. With the file's bytes in place, the gate opened.

There it ran out of time, four steps short: make sure the gate opens (which the same note says the loader fix already does), capture the expected bytes, invert pass 2 and then pass 1 with per-block keys from the emulator, and submit. On 2 November the Game Master answered HTTP 403 `event_closed`.

{{< callout type="warning" title="One address, two readings" >}}
Both takeovers captured the same registers at the same address: a byte in `rbx` and one from `rsi` XOR `rdx`. The first read the surrounding `shl`/`cmovne`/`not`/`and` sequence as a hash-map probe, making them control bytes, though it noted the `rsi ^ rdx` bytes stayed the same across inputs. The second read it as the final masked compare: `bl` the candidate, `sil ^ dl` the expected byte. The notes never reconcile the two.
{{< /callout >}}

## Dead ends

- **The seven candidates,** inverted with the constant keys: garbage.
- **Inverting the transformed input:** it returns your own input, "a no-op dressed as crypto" in the one-way note's words.
- **Forcing the success branch:** it prints the success text, then your own input.

## Takeaways

1. **Absence of evidence isn't a one-way function.** No stored flag turned up because none was stored, and the verdict sent the sessions the wrong way.
2. **Pin down what an instruction is before inverting what it touches.** One address got two readings, never settled.
3. **An emulator is only as faithful as its loader.** A 138-byte zero-fill changed the self-hash and the keys and kept the gate shut.
4. **Keep research state where a reboot can't reach it.** The first emulator died with `/tmp`; the second takeover saved its harness in the repo.
