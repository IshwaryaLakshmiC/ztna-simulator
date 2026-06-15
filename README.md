# Zero Trust Access Simulator

> **A working ZTNA policy engine with real Okta SSO integration** — sign in with your actual Okta identity, watch your real groups and MFA method populate the identity panel, then evaluate access decisions against live IdP data.

Live: **[ishwaryaaunfiltered.live/ztna-simulator](https://ishwaryaaunfiltered.live/ztna-simulator)**  
Built by [Ishwarya Lakshmi C](https://github.com/IshwaryaLakshmiC)

---

## What makes this real

When you connect your Okta developer account:

- **Your actual user** signs in via OIDC
- **Your real groups** (engineers, admins, contractors) are read from the ID token
- **Your actual MFA method** (FIDO2, TOTP, SMS) is detected from the `amr` claim
- **Auth method** is locked to `SSO via Okta ✓` — verified, not simulated
- The policy engine evaluates your **real identity attributes** against the policy rules

Device posture and network signals remain configurable — those require an MDM agent (Jamf/Intune) to pull in real-time, outside the scope of this demo.

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
- **App name:** ZTNA Simulator
- **Sign-in redirect URI:** `https://ishwaryaaunfiltered.live/ztna-simulator`  
  Also add: `http://localhost:8080` (for local testing)
- **Sign-out redirect URI:** `https://ishwaryaaunfiltered.live/ztna-simulator`
- **Controlled access:** Allow everyone (or assign specific groups)

Note your **Client ID**.

### 5. Enable Groups claim in the ID token
Security → API → Authorization Servers → **default** → Claims → **Add Claim**:
- Name: `groups`
- Include in token type: **ID Token** → Always
- Value type: **Groups**
- Filter: **Matches regex** → `.*`
- Include in: **Any scope**

### 6. Connect in the simulator
Open the simulator → enter your Okta domain and Client ID → click **Connect + Sign In**  
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

6 prebuilt scenarios covering the most common SE interview conversations:

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

Add an [OpenRouter](https://openrouter.ai) API key to get plain-English explanations of each decision — the way an SE explains a policy outcome to a non-technical customer.

Model: `mistralai/mistral-7b-instruct:free` (no cost on free tier)

---

## Running locally

**Do NOT use `python3 -m http.server`** — it serves a directory listing at `/` instead of `index.html`, breaking the Okta redirect callback.

Use one of these instead:

```bash
git clone https://github.com/IshwaryaLakshmiC/ztna-simulator
cd ztna-simulator

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

- [AWS Governance Copilot](https://github.com/IshwaryaLakshmiC/aws-governance-copilot) — AI security + cost intelligence over real AWS
- [Cloud Security Alert Automation](https://github.com/IshwaryaLakshmiC/cloud-security-alert-automation) — 8-flow n8n security operations pipeline
- [ZTNA Evaluation Framework](https://github.com/IshwaryaLakshmiC/ztna-evaluation-framework) — RFC-001: Cloudflare vs Netskope vs Palo Alto

---

**Ishwarya Lakshmi C** — Senior DevOps & Cloud Security Engineer  
[Website](https://ishwaryaaunfiltered.live) · [LinkedIn](https://linkedin.com/in/ishwaryachengalvarayan) · [GitHub](https://github.com/IshwaryaLakshmiC)
