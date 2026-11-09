# WhatsApp FAQ Support Bot (AR+EN)

**File:** `faq-customer-support-bot.json` · **Nodes:** 7 · **Status in n8n:** imported, inactive

**Kya karta hai:** Customer WhatsApp pe sawal poochta hai → AI sirf client ke FAQ document se jawab deta hai (galat info invent nahi karta). Agar jawab FAQ me nahi → customer ko polite "team member help karega" message jata hai aur sawal owner ki Google Sheet (Handoffs tab) me log ho jata hai taaki owner baad me FAQ update kar sake ya khud reply kare. Jawab customer ki language me (AR/EN auto).

**Flow:** WhatsApp Trigger → Extract → AI FAQ Answer (OpenAI) → Prepare → WhatsApp Reply → IF [HANDOFF]? → Google Sheets me log.

**Credentials chahiye (client ke):**
- WhatsApp Cloud API (Meta): phone number ID + access token — `Send Reply` node me placeholder.
- OpenAI API key — `AI FAQ Answer` node (model: gpt-4o-mini, pehle se selected).
- Google Sheets (OAuth) — `Log Handoff (Owner)` node; sheet me `Handoffs` tab (columns: phone, question, timestamp).

**Client pe deploy:** n8n me JSON import karo → FAQ node ke system prompt me `YOUR_FAQ_TEXT` ki jagah client ka asal FAQ paste karo → credentials connect karo → WhatsApp Trigger ka webhook URL client ke Meta app me register karo → workflow Active karo.

**Note:** 24-hour customer window ke andar free-form text reply chalta hai; window ke bahar template message chahiye hoga.
