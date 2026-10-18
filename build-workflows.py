#!/usr/bin/env python3
"""Build 5 sellable AR+EN n8n workflows for Zubair's agency."""
import json, os, uuid

OUT = os.path.expanduser("~/workspace/n8n/workflows")
os.makedirs(OUT, exist_ok=True)

def nid():
    return uuid.uuid4().hex[:8] + "-" + uuid.uuid4().hex[:4] + "-4000-8000-" + uuid.uuid4().hex[:12]

X = 240
def pos(i, y=300):
    return [X + i * 220, y]

def node(name, ntype, version, params, i, y=300, creds=None, webhook_id=None):
    n = {"id": nid(), "name": name, "type": ntype, "typeVersion": version,
         "position": pos(i, y), "parameters": params}
    if creds is not None:
        n["credentials"] = creds
    if webhook_id:
        n["webhookId"] = webhook_id
    return n

def wf(name, nodes, connections):
    return {"name": name, "nodes": nodes, "connections": connections,
            "pinData": {}, "settings": {"executionOrder": "v1"}, "staticData": None}

def conn(pairs):
    """pairs: list of (from, to, out_index=0)"""
    c = {}
    for frm, to, *rest in pairs:
        oi = rest[0] if rest else 0
        c.setdefault(frm, {}).setdefault("main", [])
        while len(c[frm]["main"]) <= oi:
            c[frm]["main"].append([])
        c[frm]["main"][oi].append({"node": to, "type": "main", "index": 0})
    return c

# ---------- shared builders ----------
WA_TOKEN = "Bearer YOUR_WHATSAPP_ACCESS_TOKEN"
WA_URL = "https://graph.facebook.com/v22.0/YOUR_PHONE_NUMBER_ID/messages"

def wa_send(name, i, text_expr, to_expr, y=300):
    return node(name, "n8n-nodes-base.httpRequest", 4.2, {
        "method": "POST",
        "url": WA_URL,
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "Authorization", "value": WA_TOKEN}]},
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": "={\"messaging_product\":\"whatsapp\",\"to\":\"" + to_expr + "\",\"type\":\"text\",\"text\":{\"body\":\"" + text_expr + "\"}}",
        "options": {"timeout": 10000}
    }, i, y)

def openai_reply(name, i, system_prompt, user_expr, y=300):
    return node(name, "n8n-nodes-base.openAi", 1.1, {
        "resource": "chat",
        "operation": "complete",
        "model": "gpt-4o-mini",
        "messages": {"values": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_expr}
        ]},
        "options": {"temperature": 0.7, "maxTokens": 400}
    }, i, y, creds={})

def if_node(name, i, left, op="notEmpty", right="", y=300):
    return node(name, "n8n-nodes-base.if", 2.2, {
        "conditions": {"combinator": "and", "conditions": [{
            "id": nid(), "leftValue": left,
            "operator": {"operation": op, "singleValue": True, "type": "string"},
            "rightValue": right}],
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose"}},
        "options": {}
    }, i, y)

def set_node(name, i, assignments, y=300):
    return node(name, "n8n-nodes-base.set", 3.4, {
        "assignments": {"assignments": [
            {"id": nid(), "name": k, "type": "string", "value": v}
            for k, v in assignments.items()]},
        "options": {}
    }, i, y)

def sheets_append(name, i, mapping, y=300):
    return node(name, "n8n-nodes-base.googleSheets", 4.5, {
        "resource": "sheetWithinDocument", "operation": "append",
        "documentId": {"__rl": True, "mode": "id", "value": ""},
        "sheetName": {"__rl": True, "mode": "name", "value": "Leads"},
        "columns": {"mappingMode": "defineBelow", "matchingColumns": ["phone"],
                    "schema": [], "value": mapping},
        "options": {}
    }, i, y, creds={})

# ============================================================
# 1. whatsapp-sales-agent.json
# ============================================================
SALES_SYSTEM = """You are a friendly sales assistant for a business in Saudi Arabia / UAE.
LANGUAGE RULE (strict): The customer may write in Arabic or English. ALWAYS reply in the SAME language the customer used. If they write Arabic, reply in Arabic. If English, reply in English.
أنت مساعد مبيعات ودود لشركة في السعودية / الإمارات. رد دائماً بنفس لغة العميل: عربي بالعربي، وإنجليزي بالإنجليزي.
STYLE: warm, brief (under 40 words), max 1 emoji. Ask ONE question at a time.
GOAL: learn the customer's NAME, what they NEED, and their BUDGET — one step at a time, conversationally.
When you have all three (name + need + budget), end your reply with [QUALIFIED] on its own line.
Never say you are AI. Never be pushy."""

w1_nodes = [
    node("WhatsApp In", "n8n-nodes-base.whatsAppTrigger", 1, {
        "updates": ["messages"], "options": {}}, 0, creds={}, webhook_id="wa-sales-agent"),
    set_node("Extract", 1, {
        "phone": "={{ $json.entry[0].changes[0].value.messages[0].from }}",
        "text": "={{ $json.entry[0].changes[0].value.messages[0].text.body }}",
        "profile_name": "={{ $json.entry[0].changes[0].value.contacts[0].profile.name }}"}),
    openai_reply("AI Sales Reply", 2, SALES_SYSTEM,
                 "=Customer ({{ $json.profile_name }}, {{ $json.phone }}) says: {{ $json.text }}\nReply as the sales assistant."),
    set_node("Prepare", 3, {
        "phone": "={{ $('Extract').item.json.phone }}",
        "reply": "={{ $json.choices[0].message.content.replace('[QUALIFIED]','').trim() }}",
        "qualified": "={{ $json.choices[0].message.content.includes('[QUALIFIED]') }}",
        "raw": "={{ $json.choices[0].message.content }}"}),
    wa_send("Send Reply", 4, "={{ $json.reply }}", "={{ $json.phone }}"),
    if_node("Qualified?", 5, "={{ $json.qualified }}", op="isTrue"),
    sheets_append("Log Qualified Lead", 6, {
        "phone": "={{ $json.phone }}",
        "reply": "={{ $json.raw }}",
        "timestamp": "={{ $now.toISO() }}"}, y=220),
]
w1 = wf("WhatsApp Sales Agent (AR+EN)", w1_nodes, conn([
    ("WhatsApp In", "Extract"),
    ("Extract", "AI Sales Reply"),
    ("AI Sales Reply", "Prepare"),
    ("Prepare", "Send Reply"),
    ("Send Reply", "Qualified?"),
    ("Qualified?", "Log Qualified Lead", 0),
]))

# ============================================================
# 2. appointment-booking-reminders.json
# ============================================================
CONFIRM_MSG = ("={{ 'تم تأكيد حجزك ✅\\nالخدمة: ' + $json.service + '\\nالتاريخ: ' + $json.date + ' — الوقت: ' + $json.time + '\\nسنرسل لك تذكيراً قبل الموعد.\\n\\nYour booking is confirmed ✅\\nService: ' + $json.service + '\\nDate: ' + $json.date + ' — Time: ' + $json.time + '\\nWe\\'ll remind you before your appointment.' }}")
REM24 = ("={{ 'تذكير: موعدك غداً ⏰\\n' + $json.service + ' — ' + $json.date + ' ' + $json.time + '\\nللتأكيد أرسل: نعم\\n\\nReminder: your appointment is tomorrow ⏰\\n' + $json.service + ' — ' + $json.date + ' ' + $json.time + '\\nReply YES to confirm.' }}")
REM2 = ("={{ 'موعدك بعد ساعتين 📍\\n' + $json.service + ' — ' + $json.time + '\\nنراك قريباً!\\n\\nYour appointment is in 2 hours 📍\\n' + $json.service + ' — ' + $json.time + '\\nSee you soon!' }}")
NOSHOW = ("={{ 'فاتك موعدك اليوم 😔\\nاحجز موعداً جديداً: YOUR_BOOKING_LINK\\n\\nWe missed you today 😔\\nBook a new slot: YOUR_BOOKING_LINK' }}")

w2_nodes = [
    node("Booking Webhook", "n8n-nodes-base.webhook", 2, {
        "httpMethod": "POST", "path": "book-appointment",
        "responseMode": "responseNode", "options": {}}, 0, webhook_id="book-appt"),
    set_node("Parse Booking", 1, {
        "name": "={{ $json.body.name }}",
        "phone": "={{ $json.body.phone }}",
        "service": "={{ $json.body.service }}",
        "date": "={{ $json.body.date }}",
        "time": "={{ $json.body.time }}",
        "start_iso": "={{ $json.body.date + 'T' + $json.body.time + ':00' }}",
        "wait1_h": "={{ Math.max(0.1, (new Date($json.body.date + 'T' + $json.body.time + ':00').getTime() - Date.now() - 24*3600*1000) / 3600000) }}",
        "wait2_h": "=22",
        "wait3_h": "=3"}),
    node("Create Calendar Event", "n8n-nodes-base.googleCalendar", 1.3, {
        "resource": "event", "operation": "create",
        "calendar": {"__rl": True, "mode": "list", "value": "primary"},
        "summary": "={{ $json.service + ' — ' + $json.name }}",
        "description": "={{ 'Phone: ' + $json.phone }}",
        "start": "={{ $json.start_iso }}",
        "end": "={{ new Date(new Date($json.start_iso).getTime() + 60*60000).toISOString() }}",
        "options": {}}, 2, creds={}),
    node("Respond OK", "n8n-nodes-base.respondToWebhook", 1.4, {
        "respondWith": "json", "responseBody": "={{ {status:'booked'} }}", "options": {}}, 3, y=200),
    wa_send("WhatsApp Confirm", 3, CONFIRM_MSG, "={{ $('Parse Booking').item.json.phone }}", y=400),
    node("Wait 24h Before", "n8n-nodes-base.wait", 1.1, {
        "amount": "={{ $('Parse Booking').item.json.wait1_h }}", "unit": "hours"}, 4, y=400),
    wa_send("WhatsApp Reminder 24h", 5, REM24, "={{ $('Parse Booking').item.json.phone }}", y=400),
    node("Wait 2h Before", "n8n-nodes-base.wait", 1.1, {
        "amount": "={{ $('Parse Booking').item.json.wait2_h }}", "unit": "hours"}, 6, y=400),
    wa_send("WhatsApp Reminder 2h", 7, REM2, "={{ $('Parse Booking').item.json.phone }}", y=400),
    node("Wait After Slot", "n8n-nodes-base.wait", 1.1, {
        "amount": "={{ $('Parse Booking').item.json.wait3_h }}", "unit": "hours"}, 8, y=400),
    wa_send("No-show Follow-up", 9, NOSHOW, "={{ $('Parse Booking').item.json.phone }}", y=400),
]
w2 = wf("Appointment Booking + Reminders (AR+EN)", w2_nodes, conn([
    ("Booking Webhook", "Parse Booking"),
    ("Parse Booking", "Create Calendar Event"),
    ("Create Calendar Event", "Respond OK"),
    ("Create Calendar Event", "WhatsApp Confirm"),
    ("WhatsApp Confirm", "Wait 24h Before"),
    ("Wait 24h Before", "WhatsApp Reminder 24h"),
    ("WhatsApp Reminder 24h", "Wait 2h Before"),
    ("Wait 2h Before", "WhatsApp Reminder 2h"),
    ("WhatsApp Reminder 2h", "Wait After Slot"),
    ("Wait After Slot", "No-show Follow-up"),
]))

# ============================================================
# 3. abandoned-cart-recovery.json
# ============================================================
CART1 = ("={{ 'نسيت شيئاً في سلتك! 🛒\\nخصم 10% لك: SAVE10\\nأكمل طلبك: ' + $json.checkout_url + '\\n\\nYou left something in your cart! 🛒\\n10% off for you: SAVE10\\nComplete your order: ' + $json.checkout_url }}")
CART2 = ("={{ 'آخر فرصة! ⏳ كود الخصم SAVE10 ينتهي الليلة.\\n' + $json.checkout_url + '\\n\\nLast chance! ⏳ Discount code SAVE10 expires tonight.\\n' + $json.checkout_url }}")

w3_nodes = [
    node("Cart Webhook", "n8n-nodes-base.webhook", 2, {
        "httpMethod": "POST", "path": "cart-abandoned",
        "responseMode": "responseNode", "options": {}}, 0, webhook_id="cart-abandoned"),
    set_node("Extract Cart", 1, {
        "phone": "={{ $json.body.phone }}",
        "name": "={{ $json.body.name }}",
        "cart_total": "={{ $json.body.cart_total }}",
        "checkout_url": "={{ $json.body.checkout_url }}"}),
    node("Respond OK", "n8n-nodes-base.respondToWebhook", 1.4, {
        "respondWith": "json", "responseBody": "={{ {status:'queued'} }}", "options": {}}, 2, y=200),
    node("Wait 1 Hour", "n8n-nodes-base.wait", 1.1, {"amount": 1, "unit": "hours"}, 2, y=400),
    wa_send("WhatsApp Nudge 1h", 3, CART1, "={{ $('Extract Cart').item.json.phone }}", y=400),
    node("Wait 24 Hours", "n8n-nodes-base.wait", 1.1, {"amount": 24, "unit": "hours"}, 4, y=400),
    node("Check Order Status", "n8n-nodes-base.httpRequest", 4.2, {
        "method": "GET",
        "url": "=https://YOUR-STORE.com/api/check-order?phone={{ $('Extract Cart').item.json.phone }}",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "Authorization", "value": "Bearer YOUR_STORE_API_KEY"}]},
        "options": {"timeout": 10000}}, 5, y=400),
    if_node("Purchased?", 6, "={{ $json.purchased }}", op="isFalse", y=400),
    wa_send("WhatsApp Last Chance", 7, CART2, "={{ $('Extract Cart').item.json.phone }}", y=400),
]
w3 = wf("Abandoned Cart Recovery (AR+EN)", w3_nodes, conn([
    ("Cart Webhook", "Extract Cart"),
    ("Extract Cart", "Respond OK"),
    ("Extract Cart", "Wait 1 Hour"),
    ("Wait 1 Hour", "WhatsApp Nudge 1h"),
    ("WhatsApp Nudge 1h", "Wait 24 Hours"),
    ("Wait 24 Hours", "Check Order Status"),
    ("Check Order Status", "Purchased?"),
    ("Purchased?", "WhatsApp Last Chance", 0),
]))

# ============================================================
# 4. lead-capture-instant-whatsapp.json
# ============================================================
SCORE_SYSTEM = """You are a lead scorer for a business in Saudi Arabia / UAE.
Given lead-ad data (name, phone, email, plus any answers), do two things:
1. Score: HOT (has phone + shows buying intent/budget), WARM (has phone, little info), COLD (no phone or junk).
2. Write a 1-line WhatsApp intro in the lead's language (Arabic if the name/answers are Arabic, else English), warm and under 25 words, asking ONE qualifying question about budget.
أنت مساعد تقييم عملاء لشركة في السعودية / الإمارات. قيّم العميل: HOT أو WARM أو COLD، واكتب رسالة واتساب ترحيبية قصيرة بنفس لغة العميل.
Reply ONLY valid JSON: {"score":"HOT","intro":"..."}"""

w4_nodes = [
    node("FB Lead Ads", "n8n-nodes-base.facebookLeadAdsTrigger", 1, {
        "page": "YOUR_FB_PAGE_ID", "form": "YOUR_LEAD_FORM_ID", "options": {}}, 0, creds={}),
    set_node("Extract Lead", 1, {
        "name": "={{ $json.full_name || $json.name }}",
        "phone": "={{ $json.phone_number || $json.phone }}",
        "email": "={{ $json.email }}"}),
    openai_reply("Score Lead (AI)", 2, SCORE_SYSTEM,
                 "=Lead ad data: {{ JSON.stringify($json) }}\nScore and write the intro."),
    set_node("Parse Score", 3, {
        "score": "={{ JSON.parse($json.choices[0].message.content).score }}",
        "intro": "={{ JSON.parse($json.choices[0].message.content).intro }}",
        "phone": "={{ $('Extract Lead').item.json.phone }}",
        "name": "={{ $('Extract Lead').item.json.name }}"}),
    wa_send("WhatsApp Instant Intro", 4, "={{ $json.intro }}", "={{ $json.phone }}"),
    if_node("HOT Lead?", 5, "={{ $json.score }}", op="equals", right="HOT"),
    wa_send("Notify Owner (HOT)", 6,
            "={{ '🔥 HOT LEAD: ' + $json.name + ' (' + $json.phone + ') — Score: ' + $json.score }}",
            "={{ 'YOUR_OWNER_WHATSAPP_NUMBER' }}", y=220),
]
w4 = wf("FB Lead Ads → Instant WhatsApp (AR+EN)", w4_nodes, conn([
    ("FB Lead Ads", "Extract Lead"),
    ("Extract Lead", "Score Lead (AI)"),
    ("Score Lead (AI)", "Parse Score"),
    ("Parse Score", "WhatsApp Instant Intro"),
    ("WhatsApp Instant Intro", "HOT Lead?"),
    ("HOT Lead?", "Notify Owner (HOT)", 0),
]))

# ============================================================
# 5. review-booster.json
# ============================================================
REVIEW_ASK = ("={{ 'شكراً لزيارتك ' + $json.name + '! ⭐\\nقيّم تجربتك من 1 إلى 5.\\n\\nThank you for visiting, ' + $json.name + '! ⭐\\nRate your experience from 1 to 5.' }}")
REVIEW_HIGH = ("={{ 'رائع! 🌟 شاركنا تقييمك على Google: YOUR_GOOGLE_REVIEW_LINK\\n\\nAmazing! 🌟 Please share your review on Google: YOUR_GOOGLE_REVIEW_LINK' }}")
REVIEW_LOW = ("={{ 'نأسف لسماع ذلك 🙏 أخبرنا كيف نحسّن: YOUR_FEEDBACK_FORM_LINK\\n\\nWe\\'re sorry to hear that 🙏 Tell us how we can improve: YOUR_FEEDBACK_FORM_LINK' }}")

w5_nodes = [
    node("Daily Schedule", "n8n-nodes-base.scheduleTrigger", 1.4, {
        "rule": {"interval": [{"field": "hours", "hoursInterval": 24}]},
        "options": {}}, 0),
    node("Get Yesterday's Clients", "n8n-nodes-base.googleSheets", 4.5, {
        "resource": "sheetWithinDocument", "operation": "read",
        "documentId": {"__rl": True, "mode": "id", "value": ""},
        "sheetName": {"__rl": True, "mode": "name", "value": "Appointments"},
        "options": {}}, 1, creds={}),
    if_node("Has Phone?", 2, "={{ $json.phone }}", op="notEmpty"),
    wa_send("WhatsApp Review Ask", 3, REVIEW_ASK, "={{ $json.phone }}"),
    # --- rating replies branch ---
    node("WhatsApp Rating In", "n8n-nodes-base.whatsAppTrigger", 1, {
        "updates": ["messages"], "options": {}}, 0, y=600, creds={}, webhook_id="wa-review-in"),
    set_node("Extract Rating", 1, {
        "phone": "={{ $json.entry[0].changes[0].value.messages[0].from }}",
        "rating": "={{ $json.entry[0].changes[0].value.messages[0].text.body }}"}, y=600),
    if_node("Rating 4-5?", 2, "={{ parseInt($json.rating) >= 4 }}", op="isTrue", y=600),
    wa_send("Send Google Link", 3, REVIEW_HIGH, "={{ $json.phone }}", y=520),
    wa_send("Send Feedback Form", 3, REVIEW_LOW, "={{ $json.phone }}", y=680),
]
w5 = wf("Review Booster (AR+EN)", w5_nodes, conn([
    ("Daily Schedule", "Get Yesterday's Clients"),
    ("Get Yesterday's Clients", "Has Phone?"),
    ("Has Phone?", "WhatsApp Review Ask", 0),
    ("WhatsApp Rating In", "Extract Rating"),
    ("Extract Rating", "Rating 4-5?"),
    ("Rating 4-5?", "Send Google Link", 0),
    ("Rating 4-5?", "Send Feedback Form", 1),
]))

workflows = {
    "whatsapp-sales-agent.json": w1,
    "appointment-booking-reminders.json": w2,
    "abandoned-cart-recovery.json": w3,
    "lead-capture-instant-whatsapp.json": w4,
    "review-booster.json": w5,
}
for fname, w in workflows.items():
    with open(os.path.join(OUT, fname), "w") as f:
        json.dump(w, f)
    print("wrote", fname, "| nodes:", len(w["nodes"]))
