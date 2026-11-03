{{- /*
  Challenge page archetype. Run:   hugo new huntress-ctf-2026/<catalog-key>.md
  The file name IS the catalog key (content/huntress-ctf-2026/day06-pool-party.md),
  so title, date, catalog_key and the lane defaults are filled from
  data/huntress_ctf_2026.json. scripts/ctf_new.py does the same without Hugo:
  it keeps this file's static part (the if/with blocks below count as false),
  fills the same keys itself and can list the keys that have no page yet.
*/ -}}
{{- $key := .File.ContentBaseName -}}
{{- $entry := dict -}}
{{- with hugo.Data.huntress_ctf_2026 -}}
  {{- range .challenges -}}
    {{- if eq (printf "%v" .key) $key }}{{ $entry = . }}{{ end -}}
  {{- end -}}
{{- end -}}
{{- $lane := printf "%v" ($entry.lane | default "") -}}
{{- $skills := dict "warmups" "Automation & Tooling" "metadata" "Digital Forensics" "script" "Malware Analysis" "binary" "Reverse Engineering" "mobile" "Reverse Engineering" "web" "Web Application Security" -}}
{{- $tags := dict "warmups" "encoding" "metadata" "forensics" "script" "malware-analysis" "binary" "reverse-engineering" "mobile" "android" "web" "web-exploitation" -}}
+++
# --- Filled from data/huntress_ctf_2026.json when the file name is a catalog key ---
title = "{{ $entry.title | default (replace $key "-" " " | title) }}"
date = {{ $entry.date | default $.Date }}   # the challenge's release date (today's date when the file name is not a catalog key)
draft = true                       # set to false when the write-up is ready
params.kind = "challenge"           # "kind" on its own is reserved by Hugo (removed in v0.144): keep the params. prefix
catalog_key = "{{ $key }}"{{ if not $entry.key }}   # TODO: MUST match a key in data/huntress_ctf_2026.json (this file name is not one){{ end }}
{{- with $entry.web_no }}
# web_no = {{ int . }}                      # the web lane's own numbering; shown as "Web #N" from the catalog
{{- end }}
depth = "note"                     # "full" (curated write-up) | "note" (short field note)
featured = false                   # true → appears in the hub's "Start here"

description = "One line: the key insight or the skill this shows. Used in lists, search and social cards."

# Who got it, most important first: autopilot | agent | hand | homebase
#   autopilot → "Solved by the pipeline, no human in the loop"
#   agent     → "Fixed in session by an AI coding agent (Claude Code)"
#   hand      → "Solved by hand (Austin)"
#   homebase  → "The event's Homebase AI (GPT-6 Luna) supplied the key"
# (the chips and the glance card's When column say when it was solved)
solved_by = {{ if eq (printf "%v" $entry.solved) "false" }}[]   # TODO: unsolved in the catalog{{ else }}["autopilot"]{{ end }}

tools  = []                        # e.g. ["python", "binsolve.py"] — shown at the bottom + browsable
tags   = [{{ with index $tags $lane }}"{{ . }}"{{ end }}]
skills = [{{ with index $skills $lane }}"{{ . }}"{{ end }}]   # groups it on /portfolio/

toc = true
+++

One paragraph: what the challenge asked, and what made it worth writing up.
The official prompt, the release date, the modes table and the artifact hashes
are generated from the catalog, so there is no need to repeat them here.
Never a flag, a token, a payload or a target URL: name the technique instead.

<!-- Full write-up skeleton (depth = "full"). A field note (depth = "note")
     keeps the lead paragraph, "The solve" and one takeaway. -->

<!-- ## The challenge
     What was asked and what the declared answer formats demanded. -->

<!-- ## Reading the prompt
     A clue table:  | phrase | implication | what the solver did | -->

<!-- ## What was in the files
     Formats, sizes, the structure that mattered. -->

<!-- ## The solve
     From artifact to accepted answer, step by step. -->

<!-- ## Making it deterministic
     What went into the solver so the next bundle solves itself:
     the module, the validation, the normalised spellings. -->

<!-- ## Timed modes
     Time Trial and Mastery: what changed, and what the clock did to the approach. -->

<!-- ## Dead ends
     What was tried and rejected, and what the grader taught. -->

<!-- ## Takeaways
     Two or three bullets a hiring manager can skim. -->
