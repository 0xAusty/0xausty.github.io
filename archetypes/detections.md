+++
# --- Auto-filled when you run:  hugo new detections/my-rule.md ---
title = "{{ replace .File.ContentBaseName "-" " " | title }}"
date = {{ .Date }}
draft = true

description = "One-line summary of what this rule detects and why it matters."

# --- Taxonomies (these power the filters on the Detections page) ---
# Keys are PLURAL because they're Hugo taxonomies — even when the value is singular.
mitre-techniques = ["T1059.001"]        # ATT&CK IDs this covers
platforms        = "Windows"            # Windows | Linux | macOS | AWS | Splunk | Sentinel ...
log-sources      = ["Sysmon", "Windows Security"]
tags             = ["detection-engineering"]

# Group this on /portfolio/ — omit and it will not appear there.
skills = ["Detection Engineering"]

# --- Page options ---
toc = true
+++

What behaviour does this detect, and what does an attacker have to do to trigger it?

## Detection logic

```sql
-- your rule / query here
```

## Telemetry required

Which log sources and which fields, plus any configuration needed to produce them.

## Validation

How you tested it — the exact command or tool used to generate the telemetry.

## False positives

Known benign triggers and how to tune them out.
