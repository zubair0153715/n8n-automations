# AI Invoice Processor (Accounting)

**File:** `ai-invoice-processor.json` · **Nodes:** 11 · **Status in n8n:** import-ready (not yet imported — built 2026-11-09 as a demo for an Australian accounting-practice role)

**Kya karta hai:** Invoice aate hi (webhook) uska text Gemini LLM ko bhejta hai → structured data nikalta hai (vendor, invoice number, dates, line items, subtotal, tax, total) → **totals validate karta hai** (line items ka sum = subtotal, subtotal + tax = total) → valid invoice Google Sheet (Invoices tab) mein record hoti hai (invoice_number pe upsert — duplicate nahi banta) + Slack pe notify → **invalid invoice quarantine hoti hai** + Slack alert. Koi bhi node fail ho to Error Trigger se alag alert jata hai.

**Flow:** Invoice Intake (webhook) → Prepare Extraction Prompt → Gemini Extract → Validate Totals → Valid? → [true] Record Invoice → Notify Team · [false] Quarantine → Alert Team. Error Trigger → Error Alert (alag path).

**Sheet format (Invoices tab):** columns `vendor`, `abn`, `invoice_number`, `invoice_date`, `due_date`, `currency`, `subtotal`, `tax`, `total`, `status`. `invoice_number` matching column hai — dobara wohi invoice aaye to row update hoti hai, duplicate nahi banta.

**Credentials chahiye (client ke):**
- Gemini API key — Gemini Extract node mein `YOUR_GEMINI_API_KEY` placeholder.
- Google Sheets (OAuth) — Record Invoice node; sheet ID placeholder.
- Slack incoming webhook — Notify/Alert/Error nodes mein `YOUR_SLACK_WEBHOOK_URL` placeholder.

**Test (bina n8n ke):** `tests/test_invoice_validation.py` — sample invoice + expected extraction pe wohi validation logic chalata hai jo Validate Totals node mein hai (totals recompute + duplicate check). `python3 tests/test_invoice_validation.py` → sab PASS hona chahiye (14/14). Sample files: `sample-invoice.json`, `expected-extraction.json`. **Live demo:** `node tests/demo_paddle_invoice.mjs` — workflow ka asal Validate Totals node code ek real Paddle invoice (136531-10002, $53.35) pe chalata hai: sahi invoice → Record+Notify, tampered total/line-item → Quarantine+Alert, duplicate invoice_number → update, dobara payment nahi.

**Client pe deploy:** JSON import → Gemini key, sheet, Slack webhook lagao → webhook URL ko invoice source (email parser / scanner app) se connect karo → Active. Pehli run manual "Execute Workflow" se sample invoice pe test karo.

**JD mapping (C9 AI Automation Specialist):** document processing + data extraction (Gemini), APIs/webhooks (Gemini API, Slack webhook, intake webhook), data validation + error handling (Validate Totals, Quarantine, Error Trigger), audit trail (sheet record, status column), notifications, documentation (ye README). Test data only — koi real client data nahi.
