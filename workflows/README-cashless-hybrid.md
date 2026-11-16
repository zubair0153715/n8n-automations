# Islamabad Cashless — 4-in-1 Hybrid Agents (n8n)

One importable n8n workflow that routes every incoming message to one of the
four Cashless Islamabad agents, parses it with AI, and replies on WhatsApp —
with a local Ollama fallback when the internet is down.

File: `islamabad-cashless-4-in-1-hybrid-agents.json` (9 nodes, imports inactive)

## Flow

```
Webhook POST /cashless-hub
  → Router (Switch on agent_type: khata / restaurant / onboarding / clinic)
    → Khata AI (Groq) ─┐
    → Restaurant AI ───┤
    → Onboarding AI ───┼→ Normalize Reply → WhatsApp Reply
    → Clinic AI ───────┤
    → (unknown type) ──┘
    Groq error/timeout (8s) → Ollama Fallback (localhost:11434, qwen2.5:3b)
                              → Normalize Reply → WhatsApp Reply
```

- **Online:** Groq `llama-3.3-70b-versatile` (free tier) parses the message.
- **Offline:** if Groq times out or errors, the node's error output goes to
  local Ollama (`qwen2.5:3b`). No internet needed for the fallback — but
  WhatsApp sending itself still needs internet.
- **Normalize Reply** (Code node) pulls the Roman Urdu reply out of either
  Groq (`choices[0].message.content`) or Ollama (`response`) output, so the
  WhatsApp node works for both paths.

## Setup (PKR 0, on your own PC)

1. **n8n** — install Node.js, then run:
   `npx n8n` → opens http://localhost:5678
2. **Ollama (offline AI)** — install Ollama, then run:
   `ollama run qwen2.5:3b` (listens on http://localhost:11434)
3. **Groq key (online AI, free)** — https://console.groq.com → create an API key.
4. **WhatsApp (Meta Cloud API)** — Meta Business account + WhatsApp Business
   number → phone number ID + a User Access Token (see the WhatsApp setup in
   the Khata README). Meta needs a payment method in Billing Hub for API
   messaging (Pakistan rates from 1 Oct 2026: utility/service $0.015/msg,
   first 1,000 service replies/month free).

## Import

1. n8n → Workflows → ⋯ → **Import from File** → pick this JSON.
2. It imports **inactive** — replace the placeholders first, then activate:
   - `YOUR_GROQ_API_KEY` → your Groq key (4 Groq nodes + keep it out of git;
     never commit a real key — safer: set it as an n8n env var and use
     `Bearer {{ $env.GROQ_API_KEY }}` instead).
   - `YOUR_WHATSAPP_TOKEN` → your Meta WhatsApp User Access Token.
   - `YOUR_PHONE_NUMBER_ID` → your WhatsApp Business phone number ID
     (in the WhatsApp Reply node URL).
3. Activate the workflow. Webhook URL:
   `http://localhost:5678/webhook/cashless-hub`
   (For a public URL so WhatsApp/SMS can reach it, use n8n's tunnel or put
   n8n behind a server — localhost only works on your own PC.)

## Test payloads (POST JSON to the webhook)

Khata (payment SMS):
`{"agent_type": "khata", "phone": "923001234567", "message": "Rs. 2500 received from Ahmed via Raast"}`

Restaurant order:
`{"agent_type": "restaurant", "table_no": "4", "phone": "923001234567", "message": "2 zinger aur 1 cold drink bhej dein"}`

B2B onboarding / tax:
`{"agent_type": "onboarding", "phone": "923001234567", "message": "Ali Medicos, CNIC 61101-1234567-1, today sales 45000"}`

Clinic / pharmacy:
`{"agent_type": "clinic", "phone": "923001234567", "message": "Dr. Sara ki kal shaam 6 baje ki appointment book karein"}`

`phone` must be the customer's WhatsApp number with country code, no `+`.
`phone_number_id` is taken from the WhatsApp node URL you configured, not
from the payload.

## Placeholders you MUST replace (nothing here is real)

- **Menu prices** in the Restaurant prompt are a placeholder. Only Zinger
  Burger 550 and Cold Drink 120 are verified (Mezban's own test: 2 zinger +
  1 cold drink = Rs. 1,220). Replace the menu with the restaurant's real menu.
- **Raast merchant ID** in the Clinic prompt is `DEMO-RAAST-0000` — a
  placeholder. Replace it with the clinic's real bank-issued merchant ID.
  The workflow never verifies a payment on its own; verification happens in
  the Khata app against real recorded bills.
- **CNIC / IBAN** in the Onboarding prompt are extracted only from the
  message the merchant sends, and only with their consent. Never log a full
  CNIC to a sheet or chat — mask it.

## Honest limits

- This workflow is the **routing + AI parsing + reply layer**. The four
  FastAPI apps (Khata, Mezban, Tayyar, Shifa) remain the record/dashboard
  layer — orders, bills, bookings and ledgers live there. Next step if you
  want it: POST each verified result from n8n into the apps' APIs so the
  record and the reply stay in sync.
- Offline mode covers **parsing only**. WhatsApp sending, Groq, and the
  webhook itself need internet. If the PC is off, n8n is off — for 24/7
  service the workflow needs a server (or n8n Cloud, paid).
- Groq free tier has rate limits; heavy volume will need a paid key.
- The Switch router drops payloads whose `agent_type` is not one of the
  four — those go to Normalize with a "Samajh nahi aaya" fallback reply.

## What was fixed vs the draft this is based on

- `position` fields were empty (invalid JSON) — filled in.
- Groq URL was `https://groq.com` (a website, not the API) — corrected to
  `https://api.groq.com/openai/v1/chat/completions`.
- WhatsApp URL was `https://facebook.com` — corrected to
  `https://graph.facebook.com/v21.0/<phone-number-id>/messages`.
- Error-output wiring: the draft connected the Ollama fallback as a second
  main output, which n8n does not do — each Groq node now uses
  `onError: continueErrorOutput` with output 0 → Normalize, output 1
  (error) → Ollama.
- Added the **Normalize Reply** Code node: Groq and Ollama return different
  JSON shapes, so without it the WhatsApp node would send empty text on
  one of the two paths.
- Removed the invented Raast till number (`987654321`) — replaced with the
  labelled `DEMO-RAAST-0000` placeholder.
