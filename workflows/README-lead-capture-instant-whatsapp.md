# 4. FB Lead Ads → Instant WhatsApp (AR+EN)

**File:** `lead-capture-instant-whatsapp.json` · **Status in n8n:** imported, inactive

## Kya karta hai
Facebook Lead Ad bhartay hi foran WhatsApp pe rabta — lead thanda hone se pehle.
Flow: `FB Lead Ads Trigger → Extract → OpenAI Score (HOT/WARM/COLD + intro draft) → Parse → WhatsApp instant intro → IF HOT → WhatsApp notify owner`

- AI lead ko score karta hai aur usi ki language me (AR/EN) 1-line intro likhta hai + 1 qualifying question (budget).
- HOT lead par owner ko foran WhatsApp notification (`YOUR_OWNER_WHATSAPP_NUMBER` placeholder — apna number dalein).
- AI sirf JSON me jawab deta hai: `{"score":"HOT","intro":"..."}`.

## Credentials chahiye
1. **Facebook** — Page ID (`YOUR_FB_PAGE_ID`) + Lead Form ID (`YOUR_LEAD_FORM_ID`) trigger node me; Meta app credentials n8n me.
2. **OpenAI** (`openAiApi`) — scoring ke liye.
3. **WhatsApp send** — `YOUR_PHONE_NUMBER_ID` + `YOUR_WHATSAPP_ACCESS_TOKEN` (2 nodes).

## Client pe deploy
1. Activate. 2. FB Page/Form IDs + credentials. 3. OpenAI key. 4. WhatsApp placeholders + owner number. 5. Test lead ad submit karke check karein.
