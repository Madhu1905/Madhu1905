#!/usr/bin/env python3
"""Rotate the 'security tip of the day' in README.md between the TIP markers.

Deterministic by day-of-year so the tip is stable within a day and cycles
through the list. Run by .github/workflows/daily-tip.yml (and locally).
"""
import datetime
import pathlib

TIPS = [
    "Enable MFA everywhere — it blocks the large majority of automated account-takeover attempts.",
    "Least privilege first: every account and service should have only the access it actually needs.",
    "Patch fast — most breaches exploit vulnerabilities that already had a fix available.",
    "You can't detect what you don't collect: log first, then build alerts on top.",
    "Assume breach. Design detection and response as if prevention already failed.",
    "Never trust user input — validate on the way in, encode on the way out.",
    "Keep secrets out of source code; rotate them and use a real secrets manager.",
    "Segment the network so one compromised host can't reach everything else.",
    "Back up offline — ransomware can't encrypt what it can't reach.",
    "Phishing is still the #1 entry point — verify unusual requests out-of-band.",
    "Use unique passwords per site and let a password manager remember them.",
    "Prefer allow-lists over deny-lists: enumerate the good, block the rest.",
    "Shrink the attack surface — disable unused ports, services, and accounts.",
    "Store passwords with a slow salted KDF (argon2/bcrypt), never plain text or MD5.",
    "Hunt for impossible-travel and off-hours logins to catch account takeover early.",
    "Write the incident-response runbook before you need it, not during the incident.",
    "Encrypt data in transit (TLS) and at rest by default, not as an afterthought.",
    "Audit third-party dependencies — supply-chain attacks target the weakest link.",
    "Complete mediation: check authorization on every request, every time.",
    "Threat-model early — ask 'what can go wrong?' before writing the code.",
]

START = "<!-- TIP:START -->"
END = "<!-- TIP:END -->"


def main() -> None:
    doy = datetime.date.today().timetuple().tm_yday
    idx = doy % len(TIPS)
    tip = TIPS[idx]

    block = (
        f"{START}\n"
        f"> 🔐 **{tip}**\n"
        f">\n"
        f"> <sub>Auto-rotated daily by a GitHub Action · tip #{idx + 1} of {len(TIPS)}</sub>\n"
        f"{END}"
    )

    readme = pathlib.Path("README.md")
    text = readme.read_text(encoding="utf-8")
    i = text.index(START)
    j = text.index(END) + len(END)
    updated = text[:i] + block + text[j:]

    if updated != text:
        readme.write_text(updated, encoding="utf-8")
        print(f"Updated tip -> #{idx + 1}: {tip}")
    else:
        print("No change needed.")


if __name__ == "__main__":
    main()
