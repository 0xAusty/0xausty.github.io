+++
title = "Metadata Forensics"
date = 2026-11-02
draft = true
layout = "lane"
lane = "metadata"
weight = 20

description = "A new file format almost every day and one precise field to pull out of it, from ZIP structures to registry hives: the lane where the declared answer format, not intuition, decides the spelling."

tags   = ["ctf", "forensics", "file-formats", "pe", "elf", "evtx"]
skills = ["Digital Forensics"]
toc    = true
+++

Metadata Forensics brought a new file format almost every day and asked for one precise field from it. Over the month that meant ZIP structures and hashes; JPEG, PNG and PDF headers; PE headers, version resources and entry points; .NET metadata and its MVID; MSI databases; Windows shortcuts (.lnk); OOXML packages; email headers; WAV and MP4; ELF and Mach-O headers; APK and JAR manifests; SQLite; EVTX; registry hives; Prefetch files under Xpress-Huffman compression; pcap; GPT and MBR disk images; X.509 fingerprints; duplicate-content grouping; and, on the last day, an artifact graph.

The lesson of the lane was that the declared answer format decides the spelling, not intuition: hex padded to a fixed width, a bit width where the enum value would seem the obvious choice, a GUID with braces or without them in lowercase, an array sorted or kept in file order. The right value in the wrong spelling is still rejected.

`metaengine.py`, the parser I built for this lane, grew to at least 68 format parsers by the end of the month, plus a guess-and-heal path for field names it had not seen before.
