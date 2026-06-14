# Architecture — Zero Trust Access Simulator

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Browser (Single Page App)                    │
│                                                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │  Scenario   │  │   Identity   │  │    Decision Panel     │   │
│  │  Library    │  │   Context    │  │                       │   │
│  │             │  │   Panel      │  │  ✅ ALLOW             │   │
│  │  ✅ Trusted │  │              │  │  🚫 DENY              │   │
│  │  🔴 Stolen  │  │  User/Role   │  │  🔐 STEP-UP          │   │
│  │  🟡 BYOD   │  │  MFA Status  │  │                       │   │
│  │  🟠 3am    │  │  Location    │  │  Policy Trace         │   │
│  └─────────────┘  └──────────────┘  │  MITRE ATT&CK Tags   │   │
│                                      │  AI Explanation       │   │
│  ┌──────────────────────────────┐   └───────────────────────┘   │
│  │       Device Posture         │                                 │
│  │  MDM · Patch · EDR · Encrypt │                                 │
│  └──────────────────────────────┘                                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
    ┌───────────────┐  ┌────────────┐  ┌──────────────────┐
    │  JavaScript   │  │  Okta OIDC │  │  OpenRouter API  │
    │  Policy Engine│  │  (live IdP)│  │  Mistral 7B      │
    │               │  │            │  │  (free tier)     │
    │  7 policies   │  │  Real user │  │                  │
    │  evaluated    │  │  Real MFA  │  │  Plain-English   │
    │  in order     │  │  Real groups│  │  explanation     │
    └───────────────┘  └────────────┘  └──────────────────┘
```

## Policy Evaluation Flow

```
Access Request
      │
      ▼
┌─────────────────────────────────────────────────┐
│              Policy Engine (deterministic)       │
│                                                  │
│  1. MFA check          → PASS / BLOCK / WARN    │
│  2. Auth method        → PASS / BLOCK / WARN    │
│  3. Network/location   → PASS / BLOCK / WARN    │
│  4. Device posture     → PASS / BLOCK / WARN    │
│  5. New device         → PASS / STEP-UP         │
│  6. After-hours admin  → PASS / STEP-UP         │
│  7. Risk score (0-100) → PASS / STEP-UP         │
│                                                  │
└───────────────────┬─────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ✅ ALLOW    🔐 STEP-UP   🚫 DENY
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  OpenRouter LLM  │
         │  AI Explanation  │
         │  (if key set)    │
         └──────────────────┘
```

## Okta OIDC Integration Flow

```
User clicks "Connect + Sign In"
        │
        ▼
Browser → Okta Authorization Endpoint
        │  (PKCE flow — no client secret)
        ▼
User authenticates at Okta login page
        │
        ▼
Okta → Browser redirect with auth code
        │
        ▼
Okta Auth JS SDK exchanges code for tokens
        │
        ▼
ID Token decoded:
  • name, email          → identity panel
  • groups claim         → role mapping
  • amr claim            → MFA method detection
        │
        ▼
Policy engine evaluates REAL identity
against configured policies + selected resource
```

## Identity Risk Scoring Model

```
Signal                          Max contribution
─────────────────────────────────────────────────
No MFA enrolled                      +30
SMS MFA only                         +15
TOTP MFA                             + 5
Credential stuffing pattern          +40
Local credentials (no SSO)           +10
Tor exit node                        +30
High-risk country                    +20
Unknown network                      +10
After hours                          +10
Weekend                              + 5
First-seen device                    +15
Unknown device management            +15
BYOD                                 +10
Critical patches missing             +15
No EDR installed                     +10
─────────────────────────────────────────────────
Score 0-20   → LOW      (green)
Score 21-40  → MODERATE (blue)
Score 41-70  → ELEVATED (amber)
Score 71-100 → HIGH     (red)
```

## Vendor Mapping

```
This simulator models the policy logic of:

Cloudflare Access ──── Resource + identity + device policies
Okta Adaptive MFA ──── Risk-based step-up authentication
Palo Alto Prisma ────── HIP device posture checks
Zscaler ZPA ─────────── Application segmentation
CrowdStrike Falcon ──── Endpoint device trust signals
```

## File Structure

```
ztna-simulator/
├── index.html          # Complete SPA — policy engine + Okta SDK + UI
├── docs/
│   └── ARCHITECTURE.md # This file
└── README.md           # Setup guide + Okta configuration
```
