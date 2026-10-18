# Automation-as-a-Service — Roadmap to First $1,000 MRR

Owner: Zubair Ali | Agency: AI Automation Agency | Updated: 2026-10-19

## The offer (simple)
**We install AI automations that reply to customers on WhatsApp, book appointments,
recover abandoned carts, and capture reviews — done-for-you, in Arabic + English.**

- Setup: **$300–500** one-time
- Care plan: **$99–199/month** (monitoring, tweaks, support)
- Pilot price (first 3 clients): **$200 setup** → buys us case studies

## Who buys (in order)
1. **Gulf clinics** (dental, derm, physio) — appointment booking + reminders + review booster. Saudi #1, UAE #2, Qatar #3.
2. **Gulf real estate agencies** — lead capture → instant WhatsApp qualification.
3. **E-commerce stores** (PK + Gulf) — abandoned cart recovery + WhatsApp sales agent.
4. **Restaurants/cafés** — booking + review booster.

## What we have (ready)
- 5 workflows in `workflows/` (import-ready n8n JSON + READMEs)
- `SALES-ONEPAGER.md` — buyer + pricing sheet
- 16 product promo videos in `~/workspace/your_files/`
- Harvey AI sales agent (162 prospects, triple-gate sending)

## Phase 1 — Demo assets (this week)
- [ ] Screen-record each workflow running end-to-end (30–60s clips, phone-friendly)
- [ ] 1 landing page: "AI Automations for Gulf Businesses" with clips + pricing + WhatsApp CTA
- [ ] Demo script per workflow (what to show on a 15-min sales call)

## Phase 2 — Outreach (week 2)
- [ ] Harvey: fresh prospect lists (Gulf clinics, RE agencies, e-commerce) — 3-step sequences per workflow
- [ ] Post the 16 product videos on LinkedIn + Instagram (1/day)
- [ ] DM script for warm intros; email sequences for cold
- [ ] Target: 30 outreach/day → 5+ sales calls/week

## Phase 3 — First client delivery (on first YES)
- [ ] Deploy on the CLIENT's n8n Cloud account (~$20/mo, they pay) or a Python worker on their VPS
- [ ] Client provides credentials (WhatsApp Business API, Google Sheets, calendar) — we never invent them
- [ ] Handover doc + 30-day bug-fix support included in setup
- [ ] Ask for: testimonial + permission to make it a case study

## Phase 4 — Scale (month 2+)
- [ ] Raise pilot clients to standard pricing after case study delivered
- [ ] Retainer: $99–199/mo per client for monitoring + monthly tweaks
- [ ] Referral offer: 1 month free care plan per introduced client
- [ ] 1 new workflow per month from real client requests (they fund R&D)

## Money math
- 5 clients × $150/mo avg = **$750/mo recurring** + ~$1,500 in setups
- 10 clients = **$1,500/mo recurring** — the first $1k MRR milestone
- Churn defense: the automation runs their sales — turning it off costs them money

## Rules
- Client's infrastructure, client's credentials, client's accounts. We build + maintain.
- Nothing outbound (emails/DMs) without Zubair's explicit go-ahead per batch.
- Every workflow ships with a README the client's own staff can follow.
