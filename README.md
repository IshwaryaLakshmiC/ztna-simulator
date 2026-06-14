# Zero Trust Access Simulator

> **An interactive ZTNA policy engine** — configure identity, device posture, and resource sensitivity, then evaluate access decisions in real time with a full policy trace and AI-powered plain-English explanations.

Live: **[ishwaryaunfiltered.live/ztna-simulator](https://ishwaryaunfiltered.live/ztna-simulator)**  
Built by [Ishwarya Lakshmi C](https://github.com/IshwaryaLakshmiC) · [Portfolio](https://ishwaryaunfiltered.live)

---

## What this simulates

A full Zero Trust access decision combining:

- **Identity context** — user role, MFA strength, SSO vs local auth
- **Device posture** — MDM status, patch level, EDR, encryption, browser
- **Network signals** — location, IP reputation, Tor detection, geo-risk
- **Resource sensitivity** — CRITICAL vs HIGH vs LOW classification
- **Active policies** — toggleable rules matching real Cloudflare Access / Okta Adaptive MFA behaviour

Every evaluation produces a full **policy trace** showing exactly which checks passed, failed, or triggered step-up — plus MITRE ATT&CK technique tags where relevant.

---

## Scenario library

| Scenario | Type | Expected outcome |
|----------|------|-----------------|
| Trusted employee, managed device | Legitimate | ✅ Allow |
| Stolen credentials + unknown device | Attack | 🚫 Deny |
| Contractor on personal device | Edge case | 🚫 Deny (BYOD + CRITICAL) |
| Admin access at 3am, new device | Suspicious | 🔐 Step-up |
| Executive travelling in high-risk country | Edge case | 🔐 Step-up |
| CI/CD service account | Machine identity | ✅ Allow (scoped) |

---

## Policy engine

Policies are evaluated in order. Each can be toggled on/off to simulate different organisational configurations:

1. Require MFA (blocks no-MFA users)
2. Block Tor / anonymous proxies
3. Require MDM-managed device for CRITICAL resources
4. Step-up auth on new/unrecognised device
5. Block high-risk countries (optional — off by default)
6. Step-up for after-hours admin access
7. Treat SMS MFA as insufficient for CRITICAL resources

---

## AI explanations

Add an [OpenRouter](https://openrouter.ai) API key (free tier) to enable plain-English explanations of each access decision — the same way an SE would explain a policy outcome to a non-technical customer.

Model: `mistralai/mistral-7b-instruct:free` — no cost on free tier.

---

## Running locally

Just open `index.html` in a browser. No build step, no dependencies, no server required.

```bash
git clone https://github.com/IshwaryaLakshmiC/ztna-simulator
cd ztna-simulator
open index.html   # macOS
# or: python3 -m http.server 8080
```

---

## Deploying to your domain

Copy `index.html` to your GitHub Pages repo as `ztna-simulator.html` and it serves at `yourdomain.com/ztna-simulator`.

---

## Related projects

- [AWS Governance Copilot](https://github.com/IshwaryaLakshmiC/aws-governance-copilot) — AI-powered security and cost intelligence over real AWS infrastructure
- [Cloud Security Alert Automation](https://github.com/IshwaryaLakshmiC/cloud-security-alert-automation) — 8-flow n8n security operations pipeline
- [ZTNA Evaluation Framework](https://github.com/IshwaryaLakshmiC/ztna-evaluation-framework) — RFC-001 vendor evaluation (Cloudflare vs Netskope vs Palo Alto)

---

**Ishwarya Lakshmi C** — Senior DevOps & Cloud Security Engineer  
[GitHub](https://github.com/IshwaryaLakshmiC) · [Website](https://ishwaryaunfiltered.live) · [LinkedIn](https://linkedin.com/in/ishwaryachengalvarayan)
