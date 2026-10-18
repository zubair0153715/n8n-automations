# 2. Appointment Booking + Reminders (AR+EN)

**File:** `appointment-booking-reminders.json` · **Status in n8n:** imported, inactive

## Kya karta hai
Receptionist-bot ka n8n version — booking le, confirm kare, yaad dilaye.
Flow: `Webhook (POST /webhook/book-appointment) → Parse Booking → Google Calendar event → Respond OK + WhatsApp confirm → Wait (24h pehle tak) → WhatsApp reminder 1 → Wait → WhatsApp reminder 2 (2h pehle) → Wait → No-show follow-up`

- Webhook payload: `{name, phone, service, date: "2026-10-25", time: "14:00"}`.
- Wait durations appointment time se **automatically calculate** hoti hain (tested).
- Tamam customer messages bilingual (Arabic + English) — Gulf clinics ke liye.
- No-show follow-up me `YOUR_BOOKING_LINK` placeholder hai (rebook link).

## Credentials chahiye
1. **Google Calendar** (`googleCalendarOAuth2Api`) — event banane ke liye.
2. **WhatsApp send** — HTTP nodes me `YOUR_PHONE_NUMBER_ID` + `YOUR_WHATSAPP_ACCESS_TOKEN` (4 jagah — sab me same values).
3. Webhook URL website/clinic system me lagayein.

## Client pe deploy
1. Activate karein. 2. Google Calendar connect karein. 3. WhatsApp placeholders bharein.
4. Apne booking form se webhook pe POST karein. 5. `YOUR_BOOKING_LINK` apne booking page se replace karein.
