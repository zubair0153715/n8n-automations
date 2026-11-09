# Payment Reminder — Invoice Follow-up (AR+EN)

**File:** `payment-reminder-invoice.json` · **Nodes:** 5 · **Status in n8n:** imported, inactive

**Kya karta hai:** Roz Google Sheet (Invoices tab) scan karta hai → jo invoices **unpaid** hain aur due date aa gayi hai ya guzar gayi hai, un clients ko WhatsApp pe polite reminder jata hai — due-day pe friendly reminder, uske baad din gin ke overdue notice (amount + due date + payment link). Sheet me `reminder_sent = yes` + date mark ho jati hai. Paid invoices ko kabhi touch nahi karta.

**Flow:** Daily Schedule → Google Sheets (Invoices) → Code node (unpaid + due filter, days-overdue hisaab, bilingual personalized message) → WhatsApp Reminder → Google Sheets (mark sent).

**Sheet format (Invoices tab):** columns `client`, `phone`, `amount`, `due_date` (YYYY-MM-DD), `paid` (yes/paid likhne pe skip). Workflow khud `reminder_sent` + `reminder_date` columns bhar deta hai.

**Credentials chahiye (client ke):**
- Google Sheets (OAuth) — dono Sheets nodes; sheet ID placeholder.
- WhatsApp Cloud API (Meta): phone number ID + access token — WhatsApp node me placeholder.
- Payment link: Code node ke message me `YOUR_PAYMENT_LINK` — client ka bank/JazzCash/Stripe payment link wahan lagta hai.

**Client pe deploy:** JSON import → sheet connect → WhatsApp credentials → payment link set → Active. Test: ek unpaid + kal ki due date wali test row daal ke manual Execute karo.

**Note:** Ek client ke ek se zyada unpaid invoices hain to har ek ka alag reminder jayega; sheet me mark phone pe match hota hai.
