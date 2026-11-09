# Lead Follow-up Reminder (AR+EN)

**File:** `lead-followup-reminder.json` · **Nodes:** 5 · **Status in n8n:** imported, inactive

**Kya karta hai:** Roz schedule pe Google Sheet (Leads tab) check karta hai → jin leads se **3+ din se koi contact nahi** hua (last_contact column), unko WhatsApp pe friendly bilingual follow-up bhejta hai → sheet me us lead ki `last_contact` aaj ki date se update + `followup_sent = yes` mark kar deta hai (upsert, phone pe match) — taaki kal dobara nahi bheje. Sales Agent / Lead Capture workflows ki sheet ke sath direct jorta hai.

**Flow:** Daily Schedule → Google Sheets (Leads parho) → Code node (3+ din silent filter + personalized message) → WhatsApp Follow-up → Google Sheets (mark sent).

**Sheet format (Leads tab):** columns `name`, `phone`, `last_contact` (YYYY-MM-DD). Baqi columns ignore nahi hote — Code node sirf filter karta hai.

**Credentials chahiye (client ke):**
- Google Sheets (OAuth) — dono Sheets nodes; sheet ID placeholder.
- WhatsApp Cloud API (Meta): phone number ID + access token — WhatsApp node me placeholder.

**Client pe deploy:** JSON import → sheet connect karo (client ki Leads sheet) → WhatsApp credentials → Active. Pehli run manual "Execute Workflow" se test karo (3+ din purani ek test lead daal ke).

**Note:** Follow-up promotional nature ka ho sakta hai — client ke approved template se bhejna Meta policy ke liye safe hai; text version 24h window / existing conversation ke liye hai.
