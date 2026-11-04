+++
title = "Product Placement"
date = 2026-10-13
draft = true
params.kind = "challenge"
catalog_key = "day13-product-placement"
depth = "note"
featured = false
description = "A Windows Installer ProductCode is stored as text, so the grader wanted it verbatim, braces and uppercase; the rule only surfaced two days later."
solved_by = []
tools = ["msimeta.py"]
tags = ["forensics", "metadata", "time-trial", "mastery"]
skills = ["Digital Forensics"]
toc = false
+++

The packages were small Windows Installer files that had been copied, renamed and repackaged, and each mode asked for one field, the product code GUID. It's a routine extraction. What makes it worth a note is the spelling the grader wanted.

## The solve

The notes do not record who solved this one, or how: it was unsolved at the 09:00 run, no solver change was committed for it, and the later notes only say the day was complete by 09:32 on 14 October.

What the repo does hold is `msimeta.py`, added on 14 October. It reads an MSI as an OLE compound file, decodes the compressed table stream names and the string pool, rebuilds the column-major tables and exposes the Property table as snake-cased fields, so `ProductCode` becomes `product_code`. The summary-information stream comes out of the same parser.

The product code is stored as text, so it has to be answered verbatim, braces and uppercase. Bare uppercase and lowercase were rejected when the field came back inside the Day 15 cumulative time trial, and the Day 13 reference answers, which had been stored in lowercase without a server check, were corrected afterwards.

A GUID stored as text is submitted as it is stored; only a binary GUID gets a canonical form.
