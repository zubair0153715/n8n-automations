# 3. Abandoned Cart Recovery (AR+EN)

**File:** `abandoned-cart-recovery.json` · **Status in n8n:** imported, inactive

## Kya karta hai
Adhoori chodi hui cart wale customer ko wapas lata hai.
Flow: `Webhook (POST /webhook/cart-abandoned) → Extract → Respond OK → Wait 1h → WhatsApp nudge (10% off: SAVE10) → Wait 24h → Check Order Status (HTTP) → IF not purchased → WhatsApp last-chance`

- Webhook payload: `{phone, name, cart_total, checkout_url}` (Shopify/WooCommerce se).
- Discount code `SAVE10` placeholder hai — client apna code dale.
- "Check Order Status" node me `https://YOUR-STORE.com/api/check-order` + `YOUR_STORE_API_KEY` placeholders — apne store ke hisab se configure karein. Agar store API nahi hai to ye node hata kar seedha second follow-up bhej dein (README me tareeqa likha hai — node delete karein, Wait 24h ko WhatsApp Last Chance se jor dein).

## Credentials chahiye
1. **WhatsApp send** — `YOUR_PHONE_NUMBER_ID` + `YOUR_WHATSAPP_ACCESS_TOKEN` (2 nodes).
2. Store API (optional, upar dekhein).

## Client pe deploy
1. Activate. 2. WhatsApp placeholders bharein. 3. Shopify Flow / WooCommerce webhook se cart-abandoned events POST karein. 4. Discount code apne store me banayein aur workflow me update karein.
