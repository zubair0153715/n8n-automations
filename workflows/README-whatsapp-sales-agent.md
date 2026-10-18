# 1. WhatsApp Sales Agent (AR+EN)

**File:** `whatsapp-sales-agent.json` · **Status in n8n:** imported, inactive (activate in editor)

## Kya karta hai
Customer ke WhatsApp message ka AI-powered jawab — usi language me (Arabic/English auto).
Flow: `WhatsApp Trigger → Extract (phone/text) → OpenAI sales reply → Prepare → Send WhatsApp reply → IF qualified → Google Sheets log`

- AI persona: friendly sales assistant — naam, need, budget poochta hai, ek waqt me ek sawal.
- Jab teeno mil jayein to reply ke end me `[QUALIFIED]` lagata hai → qualified lead Google Sheet me.
- System prompt bilingual hai (instructions EN+AR), reply hamesha customer ki language me.

## Credentials chahiye (sab khaali hain — client khud lagayega)
1. **WhatsApp Trigger** (`whatsAppTriggerApi`) — Meta developer app ka webhook verify token. Meta App Dashboard → WhatsApp → Configuration me webhook URL dalein (n8n editor me trigger node se milega).
2. **OpenAI** (`openAiApi`) — API key. Client chahe to Gemini se replace kar sakta hai.
3. **WhatsApp send** — HTTP node me 2 placeholders: `YOUR_PHONE_NUMBER_ID` (URL me) aur `YOUR_WHATSAPP_ACCESS_TOKEN` (Authorization header).
4. **Google Sheets** (`googleSheetsOAuth2Api`) — "Leads" sheet.

## Client pe deploy
1. n8n me workflow open → Activate toggle ON.
2. Upar wali 4 credentials connect karein.
3. Meta App me webhook URL verify karein → test message bhejein.
4. Sheet ka naam "Leads" rakhein ya node me badlein.
