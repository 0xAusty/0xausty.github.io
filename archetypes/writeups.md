+++
# --- Auto-filled when you run:  hugo new writeups/my-box.md ---
title = "{{ replace .File.ContentBaseName "-" " " | title }}"
date = {{ .Date }}
draft = true                       # set to false (or run `hugo new ... `) when ready to publish

description = "One-line summary shown in lists, search, and social previews."

# --- Taxonomies (these power the filters on the Writeups page) ---
# Keys are PLURAL because they're Hugo taxonomies — even when the value is singular.
platforms    = "Hack The Box"      # Hack The Box | TryHackMe | PortSwigger | Proving Grounds ...
oses         = ["Linux"]           # Linux | Windows | macOS  — the host OS only.
                                   # Active Directory is NOT an OS: put it in `tags`.
difficulties = "Easy"              # Easy | Medium | Hard | Insane
tools        = ["nmap", "burp"]    # shown at the bottom of the post + browsable
tags         = ["enumeration", "privilege-escalation"]   # e.g. "active-directory"

# Group this on /portfolio/ — omit and it will not appear there.
skills = ["Network Penetration Testing"]

# --- Page options ---
toc        = true                  # show the table of contents sidebar
disclaimer = true                  # show the "authorized targets only" note
+++

Intro paragraph: what the box is, why it's interesting, and the high-level path.

## Recon

{{</* terminal title="kali@htb" */>}}
$ nmap -sC -sV -oA nmap/box 10.10.10.10
{{</* /terminal */>}}

## Foothold

{{</* callout type="tip" title="Methodology note" */>}}
Explain your reasoning here so recruiters see *how* you think, not just the commands.
{{</* /callout */>}}

## Privilege Escalation

<!-- Add a screenshot: drop the file in static/images/ then uncomment:
{{</* img src="/images/your-screenshot.png" alt="describe the screenshot" caption="What this screenshot shows." */>}}
-->


## Flags

{{</* spoiler summary="Reveal the flags" */>}}
- user: `HTB{...}`
- root: `HTB{...}`
{{</* /spoiler */>}}
