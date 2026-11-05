+++
title = "Binary Reverse Engineering"
date = 2026-11-02
draft = true
layout = "lane"
lane = "binary"
weight = 40

description = "One CRC-checked config record in a dozen disguises, from C++ and .NET to Swift, Zig, WebAssembly and Neko bytecode, and the static parser that learned each new hiding place."

tags   = ["reverse-engineering", "elf", "pe", "dotnet", "java", "wasm", "crc32"]
skills = ["Reverse Engineering"]
toc    = true
+++

Day 1 was a plain C ELF asked about its headers and symbols. From Day 2 on, every daily challenge hid the same thing, a configuration record the lane called HCFG, XOR'd JSON behind a 12-byte CRC-checked header, in a new language and container each day. C++ on ELF and MinGW PE. .NET. Java and Kotlin, as Base64 inside the class-file constant pool. Go. Rust, which ships a decoy record that fails its CRC. Swift and Nim, as a Base64 string literal. Zig, in a section literally named `.hcfg`. D, Pascal, Crystal, Objective-C and WebAssembly. Overlays, a plug-in, a managed/native bridge, Neko bytecode, and two new magics. Later days added crash triage, diffing, compiler attribution and family clustering.

The bundles were cumulative from Day 3, so `binsolve.py` had to keep every earlier day's answers right while adding the new day's. On Day 8, `binmastery.py` fetched five bundles, each with a 67 MB Swift binary, solved them in parallel and submitted 400 answers in one call, about 21 s inside a roughly 27 s window.

One challenge got away: [SHA1-Hulud](/huntress-ctf-2026/day30-sha1-hulud/), a standalone Day 30 single, a stripped Rust PE with encrypted strings, anti-debug checks and four SHA-1-style functions, the month's one unsolved mode.

## What the lane kept asking for

Per member, a fixed template: a SHA-256, the format and machine or architecture, and the record's campaign, domain, mutex, URL and CRC32. The counts climbed from 24 fields on Day 3 to 434 on Day 31, when the mastery asked 6,510 over fifteen sets. The grader also went back: Day 17 added two facts for every earlier day, Day 28 structural facts about 27 days of members. From Day 19 the questions read as instructions.

## The record: HCFG

The locator's heart in `binsolve.py`, cut to its core:

```python
def hcfg(b, i):                       # i: offset of the magic
    _, ver, key, ln, crc = struct.unpack_from('<4sBBHI', b, i)
    p = bytes(x ^ key for x in b[i + 12:i + 12 + ln])
    if zlib.crc32(p) != crc:
        return None                   # a decoy, or not a record
    return {'ver': ver, 'key': key, 'crc': crc, 'cfg': json.loads(p)}
```

The CRC check is the whole defence: Rust's decoy fails it, Nim's string table holds plaintext copies of the magic, and Swift keeps a "dynamic trace" scaffold beside the real thing. Days 30 and 31 reused the layout under new magics, HGRF and HGAU, with the config nested one level down.

## Native builds: C and C++

Day 1's C ELF has no record, just a `.huntress` section and a two-instruction `recover_code`. Nothing in the repo records how Day 1 was answered; the first commit is dated 2 October. From [Day 3](/huntress-ctf-2026/day03-table-manners/) one question about it, `d01_analysis_symbols`, was the lane's longest blocker: five lists rejected, no cycling of guesses. The event's Homebase AI (GPT-6 Luna) supplied the answer on 7 October: the whole `.symtab` in stored order, empties dropped.

Day 2's C++ build asked for the mangled `score()` method and the class's vtable symbol. The ELF took bare Itanium names; the mastery's MinGW PE wanted COFF section-qualified ones. [Mangled](/huntress-ctf-2026/day02-mangled/) has the investigation.

## Managed builds: .NET, Java, Kotlin

Day 3's .NET DLL kept the record raw but cost rejections on spelling (`pe_cli`, `i386`). Java on Day 6 moved it into one `CONSTANT_Utf8` entry as Base64 text. Kotlin on Day 7 buried the same carrier among 3,000-plus stdlib classes, so the scan covers every class. Day 24's deflated jar entries defeated a raw byte scan.

## Runtimes that hide it in a string

Swift on Day 8 hid the record as Base64 in a string literal inside a 67 MB static ELF. The notes read it through the Swift String ABI; the solver finds the one Base64 run with a valid CRC ([Swift Justice](/huntress-ctf-2026/day08-swift-justice/) has both). Nim on Day 9 was Swift in a different hat. Zig went back to a raw section named `.hcfg`; D and Crystal used string literals, Pascal a constant array in `.data`, Objective-C a `.hcfg` section. After Day 10 one generic locator covered them all.

## Off the beaten path: WebAssembly and overlays

Day 16's WebAssembly pair was a format the handler didn't know; a Claude Code session's `wasm` and `wasm32` were accepted first try. Day 19 put the record in a packed `PK19` overlay and spelled out the unpack in the question; the solver transcribes it and trusts the result only when the stored digest verifies. Day 21's loader carried no record; its sibling `plugin.cmxs` member did. The misses were structural: renamed members on Day 22 cost about 16 minutes; Day 28's 30 structural re-asks, with an ELF-only first fix, about 24.

## Speaking the grader's language

`x86-64`, not `amd64`; `i386`, not `x86`; `pe_cli`, not `pe`: the grader speaks normalised. The declared format, not the field name, picks the encoding: Day 8's `elf_class` wanted the integer 64 and `machine` the raw `e_machine` 62, while Day 1's stayed text. Absence has a spelling: `[]` for a missing disassembly, `none` for a stripped symbol. Day 17's storage labels name the construct, not the section (`raw_const_array`, not `.data`), and no question listed them: the agent found them with about 900 one-field submits in about 25 minutes, the solved days' nearest brush with guessing.

<!-- Austin: confirm the framing of the Day 17 label probe ("the solved days' nearest brush with guessing"); the flagship draft flags it as closer to guessing than anything else in the event. -->

## How the solver took shape

**2 to 7 October.** The agent wrote `bresolve.py` for Day 2 on 4 October and `binsolve.py` for the whole bundle on 6 October: 47 of 48. The symbols answer on 7 October let it sweep Days 3 to 7 in every mode; the lane stood at 100% by 11:43.

**8 to 10 October.** `_hcfg_b64` for Swift and `binmastery.py` for the clock; on Day 10, Zig's section from a per-lane subagent by 09:08, the generic `_find_hcfg` handler by 09:25, then the daily sweep.

**11 to 18 October.** D solved itself, CORRECT at 09:00:07, then lost its time-trial window to a self-inflicted 429 ([How I played](/huntress-ctf-2026/how-i-played/) has that story). Day 13 was the first binary day banked in all three modes with nobody in the loop, by 09:00:43.

**19 to 31 October.** Each new twist became a day-level pass; the last two days added the HGRF and HGAU magics. Days 23, 25 and 27 ran clean at release; Day 31 finished at 09:33:08.

## Days worth knowing

- **Day 2 · [Mangled](/huntress-ctf-2026/day02-mangled/)**: the same mangled symbols, spelled differently on the ELF set and the MinGW PE.
- **Day 6 · [Pool Party](/huntress-ctf-2026/day06-pool-party/)**: one extractor for the whole bundle, and the field that held Days 3 to 7.
- **Day 8 · [Swift Justice](/huntress-ctf-2026/day08-swift-justice/)**: Base64 in a Swift string literal beside a decoy, plus the mastery runner.
- **Day 30 · [SHA1-Hulud](/huntress-ctf-2026/day30-sha1-hulud/)**: the one miss: Unicorn emulation, a wrong "one-way" verdict, a loader bug.
- **Day 17 · [Decoder Ring](/huntress-ctf-2026/day17-decoder-ring/)**: the grader as a membership oracle, about 900 one-field probes for six storage fields.
- **Day 19 · [Jack in the Box](/huntress-ctf-2026/day19-jack-in-the-box/)**: a packer reversed from its own header, CORRECT by 09:02:41.

## What the lane taught

- **Find the invariant, then the carriers.** One record format meant one module.
- **Validate with the checksum, not the magic.** The CRC alone beat the Rust and Nim decoys.
- **The declared format picks the spelling.** A right fact in the wrong vocabulary is a wrong answer.
- **Structure beat disassembly.** A 12-byte layout and a CRC check, not a disassembler, found the record everywhere.
- **A miss costs more than slow solving.** Day 15's 09:18:55 finish moved the board from 55th to 34th; Day 17's binary, solved by only eight teams, took it to 5th.
