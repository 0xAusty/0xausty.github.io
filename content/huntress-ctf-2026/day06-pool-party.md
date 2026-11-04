+++
title = "Pool Party"
date = 2026-10-06
draft = true
params.kind = "challenge"  # Hugo reserves a top-level "kind" (removed in v0.144); this still reads as .Params.kind
catalog_key = "day06-pool-party"
depth = "full"
featured = true
description = "One CRC-checked config record across C++, .NET, Go, Rust and a Java constant pool, one extractor for all five, and a symbol-table field that held out a day."
solved_by = ["agent", "homebase"]
tools = ["binsolve.py", "bresolve.py", "aeszip.py", "python"]
tags = ["reverse-engineering", "java", "elf", "pe", "dotnet"]
skills = ["Reverse Engineering"]
toc = true
+++

Pool Party was the [binary lane](/huntress-ctf-2026/lanes/binary/)'s sixth day and its turning point. Five of the six binaries in its bundle carry the same kind of configuration record, so instead of code for the new day alone, Claude Code built one extractor for the whole bundle, `binsolve.py`. It banked 47 of the 48 fields on 6 October. The last field, a list of symbols from the Day 1 ELF, had been rejected five times; the answer came on 7 October from the event's Homebase AI (GPT-6 Luna).

## The challenge

The bundle was cumulative: the 40 fields for Days 1 to 5 again, plus eight for the new Java specimen (its SHA-256, the archive container read from its final bytes, and the record's campaign, domain, mutex, URL, CRC32 and version byte, the last as an integer). The time trial asked the same 48 over a fresh bundle, the mastery 96 over two.

Two kinds of field decided the day: the format, machine and architecture fields, which take a fact only in spellings the grader recognises, and `d01_analysis_symbols`, whose templated question gave no hint of which symbols or what order.

## Reading the prompt

The title is the hint: the party is in the constant pool.

| Phrase | Implication | What the solver did |
|---|---|---|
| "its own phone book: the constant pool" | The record is a constant in a class file, readable without running anything. | `_hcfg_from_class` walks the pool, stepping over other entries by size (`Long` and `Double` take two slots), and Base64-decodes each long, Base64-only `CONSTANT_Utf8` string, keeping the one that decodes to the HCFG magic. |
| "Names, methods, invocations — it's all in there. Dive in and take attendance." | An inventory of the pool's class, method and call-site names. | Nothing on Day 6: none of the eight Java fields asked for one. The [Day 17](/huntress-ctf-2026/day17-decoder-ring/) bundle came back for the main class's method names. |

## What was in the files

`evidence.zip` is WinZip-AES encrypted with the usual password. With no 7-Zip or pip on the laptop, the pipeline opens it with `aeszip.py`, a 30-line AES-CTR and PBKDF2 extractor. Inside are the six days' binaries, named by day prefix and variant (the single's Day 1 ELF was `d01--variant-000.elf`): a C ELF, a C++ ELF, a .NET DLL with its `.runtimeconfig.json`, a Go ELF, a Rust ELF and the Day 6 jar.

The Day 1 C ELF is asked only about itself: headers, section names, symbol table and a disassembly of `recover_code`. The binaries from Days 2 to 6 carry the record the lane calls HCFG:

```text
offset  size  field
0       4     magic "HCFG"
4       1     version
5       1     XOR key
6       2     payload length (little-endian)
8       4     CRC32 of the decoded payload (little-endian)
12      n     JSON payload, every byte XOR'd with the key
```

The C++, .NET and Go builds keep it as raw bytes, which a whole-file scan for the magic finds without knowing which section holds them. The [Rust build](/huntress-ctf-2026/day05-rust-belt/) adds a decoy record with a bad CRC, there to trip a naive `find()`. The jar is the odd one out: the whole record, header included, is Base64 text in a single `CONSTANT_Utf8` entry in the constant pool of `Day06Variant000.class`.

## The solve

The release runner saw Day 6 at 09:00:09 on 6 October and logged "no solver for this lane; skipped" for binary, which joined the automated sweep only on 10 October, so the work happened in session with the agent.

`binsolve.py` decrypts the zip and answers each member by day prefix and file type: a SHA-256 per file, the formats and headers, the .NET metadata version from the BSJB metadata root, and the five HCFG records (the jar's through `hcfg_jar` and `_hcfg_from_class`).

The single was untimed, and the grader scores each submit atomically but keeps accepted answers, so the agent banked one day-group at a time and split any rejected group. Half the battle was pinning down spellings from those rejections: `x86-64` for the Go and Rust architecture, not `amd64` or `x86_64`; a lowercase `i386` for the .NET machine; the compound `pe_cli` for the .NET format.

On 6 October the single stood at 47 of 48, and the same module took the older cumulative singles to 23 of 24 (Day 3, up from 20), 31 of 32 (Day 4) and 39 of 40 (Day 5). Each was short by the same field.

`d01_analysis_symbols` had been open since the [Day 3 bundle](/huntress-ctf-2026/day03-table-manners/), and five lists had been rejected, the last on 6 October. My rule was [never to cycle guesses](/huntress-ctf-2026/how-i-played/), so the agent stopped there. The field's escalation note parked four untried hypotheses for the Homebase AI or an organiser's hint, the last of them every non-empty name in the table. Holding to the rule cost a day: the answer was already on that list.

On 7 October I put the field to the Homebase AI. Its answer was that last hypothesis, pinned down: every `.symtab` name in stored order, minus only the two empty names, keeping compiler, runtime, local, global and undefined symbols and versioned names as stored (33 names for that variant). Read afterwards, the neighbouring questions give the scope away: section names and symbols are the ELF's inventory, while a separate question names `recover_code` for disassembly. With that accepted, the single was complete, and the agent encoded the rule as one line, `[s[0] for s in e.syms if s[0]]`.

{{< callout type="tip" title="The field was an inventory, not a hunt" >}}
`d01_analysis_symbols` wanted the **entire** `.symtab` as stored, minus the empty names. Every rejected list had either kept the empties or cut the table down to the planted symbols.
{{< /callout >}}

## Making it deterministic

`binsolve.py` was committed at 11:24 on 7 October, with the sweep's results. Four things keep it from being a Day 6 script.

**It validates before it trusts.** `hcfg_from`, as committed, tries every occurrence of the magic and returns the first record whose CRC32 over the decoded payload matches, which is the whole defence against the Rust decoy:

```python
def hcfg_from(b):
    i = 0
    while True:
        i = b.find(b'HCFG', i)
        if i < 0:
            return None
        try:
            _, ver, key, ln, crc = struct.unpack_from('<4sBBHI', b, i)
            p = bytes(x ^ key for x in b[i + 12:i + 12 + ln])
            if zlib.crc32(p) == crc:
                return {'ver': ver, 'key': key, 'crc': crc, 'cfg': json.loads(p)}
        except Exception:
            pass
        i += 1
```

**It handles config binaries by day prefix, not file type.** A mastery set can swap the Day 2, 4 or 5 binary for a byte-patched Windows PE copy, so the format comes from the magic (`\x7fELF` or `MZ`) and the record from the raw bytes.

**It scans every class in a jar**, those containing `SENGR` first, because the Base64 of the HCFG magic always starts that way. That scan was added the next day, when the [Day 7 Kotlin jar](/huntress-ctf-2026/day07-routine-check/) buried its carrier among 3,000+ classes.

**It keeps the grader's vocabulary:** `x86-64`, `i386`, `pe_cli`, `jar`, and lowercase `0x` hex padded to eight digits for the CRC32 and two for the XOR key. Not everything was parsed, though: the Day 1 header answers, the .NET format and machine, and the Go and Rust architecture were constants, not values read from the headers. They held in all three modes.

## Timed modes

Neither timed mode added a new kind of field; what changed was the order of work. The grader locks the time trial until the single is CORRECT and the mastery until the time trial is, and a timed mode is submitted only with every field solved, so both waited for the symbols field.

The same runner covers every mode: `python3 binsolve.py` with `/time_trial` or `/mastery` appended sends a timed mode's fields in one call and fetches one bundle per `setN.` prefix for a mastery. Both modes were CORRECT by 11:24 on 7 October, when the commit recorded the sweep of every binary mode from Day 3 to Day 7. Per-mode times were not recorded.

## Dead ends

- **Five symbol lists.** The planted symbols are `marker`, `recover_code` and `main`. Rejected before Day 6: the whole `.symtab` with its empty names, the three planted names alphabetically and in table order, and `main` with `recover_code`. Rejected on 6 October: the planted pair `marker` and `recover_code`. The first of those held every right name plus the two empty strings.
- **Spellings outside the grader's vocabulary.** Rejected: bare `pe` for the .NET format (before Day 6), and `x86`, `I386` and `MSIL` for its machine.

## Takeaways

1. **Find the invariant, then the carriers.** One record format in five builds meant one module, which also lifted three older singles.
2. **Validate with the checksum, not the magic.** The CRC32 alone separates the Rust record from its decoy.
3. **The declared format decides the spelling.** A correct fact in the wrong vocabulary is a wrong answer.
4. **When a complete answer is rejected, check what is extra before cutting scope.** Every narrower symbol list was further from the answer than the full table.
