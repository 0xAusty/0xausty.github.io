+++
title = "Trust the Webhook"
date = 2026-10-26
draft = true
params.kind = "challenge"  # Hugo reserves a top-level "kind" (removed in v0.144); this still reads as .Params.kind
catalog_key = "day26-trust-the-webhook"
depth = "full"
featured = false

description = "A webhook dispatcher that verified no signature, and an hour lost to a proof scanner that only knew the token shape and missed the evidence field."

solved_by = ["homebase", "agent"]

tools  = ["websolve.py", "python"]
tags   = ["web-exploitation", "webhook", "mastery"]
skills = ["Web Application Security"]

toc = true
+++

Trust the Webhook was the [web lane](/huntress-ctf-2026/lanes/web/)'s nineteenth target, and its best reversal. The app was an event dispatcher, and the vulnerability was exactly the one the prompt advertises: it verifies nothing before it believes an event. The pipeline reached the right request during an hour of probing and still read it as a miss, because the proof came back in a field the scanner was not looking at. The hour went to a wrong assumption baked into the tooling. The event's Homebase AI (GPT-6 Luna) got past it, and its recipe was folded in so the class could never miss again.

## The challenge

Web targets are live and expire, so there is nothing to download: the proof sits on the target. The single asked one field, recover the proof from Target 1, and the time trial asked the same field against a fresh target under the clock. The mastery bundled four different apps, none of them the single's webhook route; one was a search SQL injection.

The target was a dispatcher that takes inbound event notifications and acts on them. A disclosed clues endpoint, read-only recon, named the three values the app wanted to hear: the event type it expected, the owner scope and the current role.

## Reading the prompt

For once the prompt named the mechanism outright.

| Phrase | Implication | What the solver did |
|---|---|---|
| "believes every event it's told about" | No provenance check: the app trusts the event body, not its origin. | Treated the dispatcher as unauthenticated and looked for the route that acts on an event. |
| "Tell it a convincing enough story" | The forgery is a well-formed event body, not a cryptographic bypass. | Resubmitted the disclosed clue values under the keys the handler reads. |
| "act on your forged news" | Acting on the event is what releases the proof. | Read the dispatcher's reply, where the proof was returned. |

## What was in the files

There was nothing to unpack: the surface was the live app and its disclosed clues. The class is a missing signature check, which makes it an integrity defect. A real webhook receiver verifies that an event came from the sender it claims to: typically an HMAC over the raw body against a shared secret, compared in constant time, with a timestamp or nonce to stop replay. This dispatcher did none of that. It read the event type, the owner scope and the role straight from the body and acted on them. So the recon was the attack surface: the clues endpoint handed over the exact values a genuine sender would have signed, and there was no signature to forge.

## The solve

With no signature to defeat, the work was to send the dispatcher an event that told the story it wanted, the disclosed event type, owner scope and role under the three short keys the handler reads, and take the proof out of its reply.

That is where an hour disappeared. The automated probing was sending the right event body and getting the right answer back, but the answer rode in an `evidence` field in the JSON reply rather than as a bare prefixed proof token in the page. The scanner only knew how to recognise the token shape, so it saw a reply with no proof and recorded a miss, over and over.

The way through came from outside the pipeline. The challenge went to the Homebase AI with the Game Master's prompt quoted word for word, the same framing that had [unlocked Expansion Pack](/huntress-ctf-2026/day03-expansion-pack/) three weeks earlier. The Homebase AI solved all three modes itself and handed back the recipe: no signature check, resubmit the disclosed values, and the proof is the `evidence` field. The modes were still open at 11:00:01; the single went CORRECT at 12:23:00, the time trial at 12:24:01 and the mastery at 12:30:09, and the supervisor showed the day complete by 18:14:32.

{{< callout type="warning" title="The request was right; the reader was wrong" >}}
The pipeline hit the correct event body during that hour and kept scoring it a miss, because its proof scanner recognised only a prefixed token and the real proof sat in an `evidence` field. The blind spot was an assumption in the tooling.
{{< /callout >}}

## Making it deterministic

The coding agent, Claude Code, folded the recipe into `websolve.py` as `solve_webhook`, committed at 17:16 on 26 October. It reads the disclosed values from the clues endpoint, sends the event, and takes the proof from the reply's `evidence` field, with the old token scan kept only as a fallback for when that field is absent. The read, as committed:

```python
proof = None
try:
    j = r.json()
    if isinstance(j, dict) and isinstance(j.get("evidence"), str):
        proof = j["evidence"]
except ValueError:
    pass
```

A branch in the lane's `classify` routes a target to the webhook procedure when its clues carry an event type and an owner scope, placed after the serialised-state check. Web has no artifact and its targets expire, so the lane sits outside the offline replay gate and is checked by a live self-test instead.

## Timed modes

The time trial was the same single field against a fresh target, under the clock. The mastery bundled four different apps, none of them the single's webhook route; one was a search SQL injection that needed a parenthesised payload. All three modes were solved by the Homebase AI, and the fold-in came after, at 17:16, with the request body checked against its confirmed recipe. The mastery reinforced a rule the lane already had: classify each target in a bundle on its own, and recon each one before reusing a pattern.

## Dead ends

- **An hour of black-box probing with a proof-token scanner.** This was the only real obstacle. The probing reached the right request during that hour, but the proof scanner had been built around a prefixed token shape and never looked at the `evidence` field, so a correct solve read as a miss. It cost rank: the notes record the main-board rank at 66th after Day 26, down from 5th after Day 17, and put the slide down to late finishes, of which this was the latest.

## Takeaways

1. **An integrity failure is a missing check.** There was no signature to break. The defence that was missing, verifying the sender before acting, is the whole lesson.
2. **The tool's assumptions are part of the attack surface.** The pipeline could send the right request and still fail, because it recognised only one shape of answer. The fix was to widen what it reads.
3. **Fold in the correction as well as the answer.** The recipe became `solve_webhook` and a `classify` branch the same afternoon, so the blind spot that cost an hour could not recur for this class.
