# Order Status Tracker (AR+EN)

**File:** `order-status-tracker.json` · **Nodes:** 9 · **Status in n8n:** imported, inactive

**Kya karta hai:** Store (Shopify/WooCommerce/Salla) se order status change ka webhook aata hai → customer ko WhatsApp pe automatic update: **Shipped** (tracking link ke sath), **Out for Delivery**, **Delivered** — teeno messages Arabic + English. Status values normalize ho jate hain (`Out for delivery`, `out-for-delivery` → `out_for_delivery`), is liye platform ke exact format pe depend nahi karta.

**Flow:** Order Webhook (`POST /webhook/order-update`) → Extract Order → Respond OK (webhook ko foran jawab, IF chain ke parallel) → IF Shipped? → WhatsApp / IF Out for Delivery? → WhatsApp / IF Delivered? → WhatsApp.

**Webhook payload (store se):** `{ "order_id": "...", "phone": "9665...", "name": "...", "status": "shipped | out_for_delivery | delivered", "tracking_url": "https://..." }`

**Credentials chahiye (client ke):**
- WhatsApp Cloud API (Meta): phone number ID + access token — teeno WhatsApp nodes me placeholder.
- Store side: order-status webhook is URL pe point karna (Shopify Flow / WooCommerce webhook / Salla-Zid automation) — koi API key yahan nahi chahiye.

**Client pe deploy:** JSON import → WhatsApp placeholders client ke Meta credentials se bharo → workflow Active → production webhook URL store admin me lagao → test order se 3 statuses verify karo.

**Note:** Promotional nahi, transactional updates hain — phir bhi 24h window ke bahar bhejne ke liye Meta-approved utility template use karna behtareen practice hai.
