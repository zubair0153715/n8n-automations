# 5. Review Booster (AR+EN)

**File:** `review-booster.json` · **Status in n8n:** imported, inactive

## Kya karta hai
Khush customer se Google review, naraaz se private feedback — automatically.
Do hisse, ek workflow me:
- **Part A (daily):** `Schedule (24h) → Google Sheets (Appointments sheet parhein) → IF phone → WhatsApp: "Rate 1-5"`
- **Part B (replies):** `WhatsApp Trigger → Extract rating → IF >= 4 → Google review link` / `else → private feedback form link`

- `YOUR_GOOGLE_REVIEW_LINK` aur `YOUR_FEEDBACK_FORM_LINK` placeholders hain.
- Rating "1"-"5" text reply se aati hai.

## Credentials chahiye
1. **Google Sheets** (`googleSheetsOAuth2Api`) — "Appointments" sheet (columns: name, phone).
2. **WhatsApp Trigger** (`whatsAppTriggerApi`) — Meta webhook verify.
3. **WhatsApp send** — `YOUR_PHONE_NUMBER_ID` + `YOUR_WHATSAPP_ACCESS_TOKEN` (3 nodes).

## Client pe deploy
1. Activate. 2. Sheets + WhatsApp credentials. 3. Google review link (Google Business profile se) aur feedback form link (Google Form) dalein. 4. Appointments sheet roz update ho (ya booking workflow se jor dein).
