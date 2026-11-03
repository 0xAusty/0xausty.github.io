+++
title = "Binary Reverse Engineering"
date = 2026-11-02
draft = true
layout = "lane"
lane = "binary"
weight = 40

description = "One config record, a dozen disguises: the same CRC-checked HCFG blob hidden in C, C++, .NET, Java, Kotlin, Go, Rust, Swift, Nim, Zig, WebAssembly and more, extracted deterministically every day."

tags   = ["reverse-engineering", "elf", "pe", "dotnet", "java", "webassembly"]
skills = ["Reverse Engineering"]
toc    = true
+++

Every binary in this lane hid the same thing: a configuration record called HCFG, a 12-byte header with a version, an XOR key, a length and a CRC32, followed by XOR'd JSON. What changed each day was the language and the container. C and C++ on ELF and on MinGW PE. .NET. Java and Kotlin, with the record as Base64 inside the class-file constant pool. Go. Rust, which ships a decoy record that fails its CRC. Swift and Nim, as a Base64 string literal. Zig, in a section literally named .hcfg. D, Pascal, Crystal, Objective-C and WebAssembly. Packed overlays (PK19, RS20), shared-library plug-ins, managed/native bridges and Neko bytecode. Around the record itself, the lane also asked for crash triage, patch and variant diffing, compiler attribution and family clustering.

The bundles were cumulative, so the lane's deterministic extractors, `binsolve.py` and `binmastery.py`, had to keep every earlier day's answers right while adding the new day's. The timed masteries turned that into a logistics problem as well: several 67 MB bundles to download and solve in parallel.

One challenge got away. SHA1-Hulud, the standalone Day 30 challenge, was a Rust PE with self-decrypting code and SHA-1 variants, and it was the one challenge of the month that was not solved.

<!-- Outline. Source: WRITEUP_NOTES.md entries for Days 1-19 (binary beats), binsolve.py / bresolve.py.
     Link back to the flagship: /projects/huntress-ctf-2026-ai-arena/ -->

<!-- Intro: the binary lane, cumulative bundles that re-ask every earlier day, and the one record every build hides. (outline note: the intro paragraphs above now cover this) -->

## The record: HCFG

<!-- Magic, version, XOR key, length, CRC32 header, then XOR'd JSON. Show the struct layout and a
     ten-line Python decoder. The CRC check matters: the Rust build ships a decoy HCFG with a bad CRC
     to trip a naive find(). -->

## Native builds: C and C++

<!-- Day 1 C ELF: the config in its own section. The d01 symbols field wanted the entire .symtab in
     stored order (my solve). Day 2 C++ on ELF vs PE: mangled names, and MinGW's COFF
     section-qualified names (.text$_ZNK15DiscoveryEngine5scoreEPKc). Same symbol, different container,
     different expected string. -->

## Managed builds: .NET, Java, Kotlin

<!-- .NET PE: the grader wants pe_cli and i386. Java "Pool Party": the HCFG is base64 inside a
     CONSTANT_Utf8 in the class-file constant pool. Kotlin: the same trick inside a 5 MB jar with
     3,000+ stdlib classes, so scan for the class that carries the blob. -->

## Runtimes that hide it in a string

<!-- Go and Rust (the decoy). Swift: a 67 MB static ELF; follow encodedConfig(), read the Swift
     String ABI out of the two return registers (count 0x1fc = 508, pointer into rodata), pull exactly
     those 508 base64 chars. The "dynamic trace" decoy next to it. Nim: same pattern as Swift.
     Zig: back to a raw section, literally named .hcfg. -->

## Off the beaten path: WebAssembly and a packer

<!-- Day 16 WebAssembly (direct and compact builds): wasm / wasm32, everything accepted first try.
     Day 19 PK19 overlay at the end of the ELF: length, sha256, rotate-and-xor back to HCFG,
     transcribed straight from the challenge text. -->
<!-- TODO: Days 20-31 binary formats. -->

## Speaking the grader's language

<!-- x86-64 not amd64, i386 not x86, pe_cli not pe. elf_class wanted 64 (bit width), not the EI_CLASS
     enum 2, while machine wanted the raw e_machine 62. Padded hex (0x00065bd0). [] or none for an
     absent symbol. Lesson: the declared answer_format picks the encoding, not intuition. -->

## Takeaways

<!-- Find the invariant (the record), then learn each container's way of hiding it. Validate with
     the checksum, not the magic. Parse with struct; no disassembler was needed for the config. -->
