# Identity & Access Decision Studio

> **An interactive identity and access decision platform** — evaluate policy impact, access risk, compliance alignment, and rollout decisions before production enforcement. Sign in with a real Okta identity, watch your actual groups and MFA method populate the identity panel, then see policy decisions evaluated against live IdP data.

Live: **[ishwaryaaunfiltered.live/identity-access-decision-studio](https://ishwaryaaunfiltered.live/identity-access-decision-studio)**
Built by [Ishwarya Lakshmi C](https://github.com/IshwaryaLakshmiC)

---

## What this is

Most access-control demos either fake the identity layer or hide the decision logic behind a black box. This one does neither — it's built to support the actual conversations a Solutions Engineer has with a platform, security, or infrastructure team:

- **Will this policy break anyone before we enforce it?** → Policy Impact Analysis simulates the blast radius across a sample user population before rollout
- **Are we actually covered for our compliance framework?** → Compliance Mapping shows live status against CIS, NIST, SOC2, and ISO 27001
- **What would leadership need to see?** → CISO Executive View turns policy decisions into board-level reporting
- **Why was this specific request allowed or denied?** → Access Decision shows the full evaluation trace, not just a verdict

The identity and policy evaluation underneath happens to be built on Zero Trust and adaptive access concepts — but the platform itself is broader than any one vendor category. The same decision model applies whether the conversation is about identity (Okta), access policy (Cloudflare), data governance (Databricks), or platform security posture (Wiz).

---

## What makes this real

When you connect your own Okta developer account:

- **Your actual user** signs in via OIDC
- **Your real groups** (engineers, admins, contractors) are read from the ID token
- **Your actual MFA method** (FIDO2, TOTP, SMS) is detected from the `amr` claim
- **Auth method** is locked to `SSO via Okta ✓` — verified, not simulated
- The policy engine evaluates your **real identity attributes** against the policy rules

Device posture and network signals remain configurable — those require an MDM agent (Jamf/Intune) to pull in real time, outside the scope of this demo.

---

## Capabilities

| Capability | What it shows |
|---|---|
| Access Decision | Real-time policy evaluation against live identity, device, and network signals — full trace, not just allow/deny |
| Policy Impact Analysis | Blast-radius simulation across a sample user population before a policy ships |
| Compliance Mapping | Live status against CIS Controls, NIST CSF, SOC2, and ISO 27001 |
| CISO Executive View | Board-level reporting: risk trends, access volume, top deny reasons |
| Scenario Library | 6 prebuilt identity/access scenarios covering common SE conversations |
| Rollout Recommendations | Phased-rollout guidance generated from simulated policy impact |

---

## Okta setup (5 minutes)

### 1. Create a free developer account
[developer.okta.com](https://developer.okta.com) → Create Free Account
Your domain: `dev-XXXXXXXX.okta.com`

### 2. Create test users
Directory → People → Add Person:

| Name | Email | Password |
|------|-------|----------|
| Sarah Chen | sarah.chen@test.com | set a password |
| John Admin | john.admin@test.com | set a password |
| Contractor Ext | contractor.ext@test.com | set a password |

### 3. Create groups and assign users
Directory → Groups → Add Group: `engineers`, `admins`, `contractors`, `executives`
Assign users to groups accordingly.

### 4. Create an OIDC application
Applications → Create App Integration → **OIDC** → **Single Page App**

Settings:
- **App name:** Identity & Access Decision Studio
- **Sign-in redirect URI:** `https://ishwaryaaunfiltered.live/identity-access-decision-studio`
  Also add: `http://localhost:8080` (for local testing)
- **Sign-out redirect URI:** `https://ishwaryaaunfiltered.live/identity-access-decision-studio`
- **Controlled access:** Allow everyone (or assign specific groups)

Note your **Client ID**.

### 5. Enable Groups claim in the ID token
Security → API → Authorization Servers → **default** → Claims → **Add Claim**:
- Name: `groups`
- Include in token type: **ID Token** → Always
- Value type: **Groups**
- Filter: **Matches regex** → `.*`
- Include in: **Any scope**

### 6. Connect in the studio
Open the app → enter your Okta domain and Client ID → click **Connect + Sign In**
You'll be redirected to Okta's login page. Sign in. You're back with your real identity loaded.

---

## Policy engine

7 policies, all toggleable:

| Policy | Default | Effect |
|--------|---------|--------|
| Require MFA | ON | Blocks users with no MFA enrolled |
| Block Tor / proxies | ON | Denies all Tor exit node traffic |
| Require MDM for critical | ON | BYOD/unknown devices blocked from CRITICAL resources |
| Step-up on new device | ON | First-seen devices require additional verification |
| Block high-risk countries | OFF | Geo-block policy (toggle to test executive travel scenario) |
| Step-up after-hours admin | ON | Admin access outside business hours requires confirmation |
| SMS MFA insufficient for critical | ON | SMS-only MFA denied on CRITICAL resources |

---

## Scenario library

6 prebuilt scenarios covering common identity and access conversations:

| Scenario | Type | Verdict |
|----------|------|---------|
| Trusted employee, managed device | Legitimate | ✅ Allow |
| Stolen credentials + unknown device | Attack | 🚫 Deny |
| Contractor on personal device (BYOD) | Edge case | 🚫 Deny |
| Admin access at 3am, new device | Suspicious | 🔐 Step-up |
| Executive travelling in high-risk country | Edge case | 🔐 Step-up |
| CI/CD service account | Machine identity | ✅ Allow |

With Okta connected: scenarios load device/resource context only — identity comes from your live Okta session.

---

## AI explanations

Each access decision includes a plain-English explanation generated server-side — the way an SE would explain a policy outcome to a non-technical stakeholder. This calls a shared backend endpoint (the same Bedrock → Groq → Gemini → OpenRouter fallback chain used across this portfolio's other projects), so no API key is required to use this feature.

---

## Running locally

**Do NOT use `python3 -m http.server`** — it serves a directory listing at `/` instead of `index.html`, breaking the Okta redirect callback.

Use one of these instead:

```bash
git clone https://github.com/IshwaryaLakshmiC/identity-access-decision-studio
cd identity-access-decision-studio

# Option A — Python (no install needed)
python3 serve.py

# Option B — Node.js (no install needed)
node server.js

# Option C — npx
npx serve . -l 8080 -s
```

Then open **http://localhost:8080/**

The Okta redirect URI to whitelist in your app settings: **`http://localhost:8080/`** (with trailing slash)

---

## Related portfolio projects

- [Security Discovery & Solution Design Copilot](https://github.com/IshwaryaLakshmiC/security-discovery-copilot) — AI-driven discovery, gap analysis, and architecture tradeoff engine
- [AWS Governance Copilot](https://github.com/IshwaryaLakshmiC/aws-governance-copilot) — AI security + cost intelligence over real AWS
- [Cloud Security Alert Automation](https://github.com/IshwaryaLakshmiC/cloud-security-alert-automation) — 8-flow n8n security operations pipeline

---

**Ishwarya Lakshmi C** — Cloud Infrastructure Architect · Platform Engineer · Solutions Engineering
[Website](https://ishwaryaaunfiltered.live) · [LinkedIn](https://linkedin.com/in/ishwaryachengalvarayan) · [GitHub](https://github.com/IshwaryaLakshmiC)
