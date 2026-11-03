+++
title = "Pool Party"
date = 2026-10-06
draft = true
params.kind = "challenge"  # Hugo reserves a top-level "kind" (removed in v0.144); this still reads as .Params.kind
catalog_key = "day06-pool-party"
depth = "full"
featured = true
description = "The same hidden config record in a C ELF, a .NET PE, Go, Rust and a Java constant pool, one deterministic extractor for all of them, and the symbol-table field that fell a day late."
solved_by = ["agent", "hand"]
tools = ["python"]
tags = ["reverse-engineering", "java", "elf", "pe", "dotnet"]
skills = ["Reverse Engineering"]
toc = true
+++

## The challenge

Day 6 of the binary lane, Game Master id `binary-reverse-engineering-day-06-java-bytecode-loader`. The single asked 48 fields (28 exact text, 16 pattern, 3 JSON, 1 integer) over one `evidence.zip` of 1,919,090 bytes; the time trial asked the same 48 over a fresh zip, and the mastery asked 96 over two sets. All three modes came back CORRECT, 10 of 10 points.

The lane was cumulative. The Day 6 bundle covered Days 1–6: an ELF built from C, a .NET PE, Go, Rust and the new Java jar. Every one of them hides the same configuration record, which the lane calls HCFG: JSON XOR'd with a key, behind a small header that includes a CRC32. The day's addition was where the Java jar keeps it, and the title says so: the constant pool.

## Reading the prompt

The prompt is quoted in full in the card above. Three phrases carry the puzzle:

| Phrase | Implication | What the solver did |
|---|---|---|
| "its own phone book: the constant pool" | The record is a constant-pool entry inside a class file, not a resource in the jar and not something assembled at runtime. | Parsed each class file's constant pool, Base64-decoded the `CONSTANT_Utf8` entries and kept the one whose HCFG header and CRC32 check out. |
| "Names, methods, invocations — it's all in there" | The identifiers the questions ask for are static too; the pool holds them, so nothing has to run. | — <!-- TODO: which of the 48 fields asked for Java class names, methods and invoked methods, and how binsolve.py answered them --> |
| "take attendance" | The questions are an inventory. The declared answer formats (28 exact text, 16 pattern, 3 JSON, 1 integer) say how each item has to be spelled. | Emitted every value in the grader's normalised vocabulary rather than the toolchain's (see "Dead ends"). |

## What was in the files

`evidence.zip` was WinZip-AES encrypted. The laptop had no 7-Zip, so the pipeline opens these archives itself with a small AES-CTR + PBKDF2 routine; after that it is an ordinary zip holding the cumulative bundle.

<!-- TODO: the file names inside evidence.zip and which binary belongs to which day -->

Where each binary keeps the record, as far as the notes go:

- **Java jar (Day 6).** Base64 inside a `CONSTANT_Utf8` entry of a class file's constant pool. Decode the entry and it is the same header-plus-XOR'd-JSON as every other day.
- **Rust.** A decoy HCFG record with a bad CRC32, placed to trip a naive byte search.
- **ELF (C), .NET PE, Go.** <!-- TODO: how each of these carries the record -->

## The solve

Rather than a Day 6 script, I had the coding agent build one deterministic extractor for the whole bundle, `binsolve.py`, in session that day. It locates the HCFG record in each binary, checks the CRC32 so the Rust decoy is skipped, decodes the JSON and fills the fields from it. The first full submission banked 47 of 48, and because the bundle was cumulative the same extractor pulled the older binary singles up with it: Day 3 went from 20 correct to 23 of 24, Day 4 to 31 of 32 and Day 5 to 39 of 40.

The field that held out was `d01_analysis_symbols`, the Day 1 ELF's symbol list. It fell the next day, once I had worked out what the grader wanted; that reading was mine, not the agent's.

{{< callout type="tip" title="The field was an inventory, not a hunt" >}}
`d01_analysis_symbols` wanted the **entire** ELF `.symtab`, in the order the file stores it, with empty names dropped, not the planted subset. Once the extractor listed the table instead of selecting from it, the last field closed and the single was 48 of 48.
{{< /callout >}}

## Making it deterministic

The extractor had to keep every earlier day right while adding the new one, and it had to work on variants it had never seen. Four rules did that:

- **Read the record from raw bytes.** The mastery's second set shipped the config binaries as byte-patched Windows PE copies, so the extractor reads the HCFG record out of the bytes regardless of whether the container is an ELF or a PE.
- **Validate before trusting.** The CRC32 in the header is checked; a record that fails it is a decoy, not an answer.
- **Spell it the grader's way.** The declared answer format decides the spelling: `x86-64` (not `amd64` or `x86_64`) for the Go and Rust ELFs, `i386` in lowercase for the .NET PE's machine, and `pe_cli` (not `pe`) for the .NET format.
- **Keep the zip handling in the pipeline.** WinZip-AES decryption is done in code, so a solve never waits on a tool that is not installed.

## Timed modes

The time trial asked the same 48 fields over a fresh `evidence.zip` (1,919,109 bytes) and came back CORRECT. The mastery asked 96 fields across two sets, each its own `evidence.zip` of 1,919,111 bytes, and also came back CORRECT; its second set is the one with the byte-patched PE copies, which the raw-bytes rule above is there for.

<!-- TODO: when each timed mode was confirmed and how long the solve took; the catalog carries no confirmed_at for Day 6 -->

## Dead ends

- **A byte search for the record.** In the Rust binary it lands on the decoy first; the CRC32 is what tells the two apart.
- **The toolchain's spellings.** `amd64`, `x86_64` and `pe` describe the files correctly and are not what the grader accepts.
- **The planted symbols.** Answering `d01_analysis_symbols` with the planted subset instead of the whole `.symtab` cost a day.

<!-- TODO: anything else tried and rejected on Day 6; the notes record only the three above -->

## Takeaways

1. **The declared format decides the spelling.** Derive the fact, then write it the grader's way; a correct fact in the wrong vocabulary is a wrong answer.
2. **Validate what you find.** A CRC32 check is cheap, and here it was the only thing separating the record from the decoy.
3. **When a field keeps failing, question the scope before the answer.** The whole `.symtab`, not the interesting part of it.
4. **Parse bytes, not containers.** The extractor handled the ELF, the .NET PE and the byte-patched PE copies without caring which it was given.
