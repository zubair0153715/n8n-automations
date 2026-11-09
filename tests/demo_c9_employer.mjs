// Employer demo (C9 Teams): run the AI Invoice Processor end-to-end the way
// C9's team would see it — invoice in, Sheets row + Slack message out.
// The "Validate Totals" step runs the REAL node code from the workflow.
// The "Gemini Extract" step shows the exact JSON the workflow expects
// (simulated here — a live Gemini call needs an API key, which is not
// connected in this demo). Usage: node tests/demo_c9_employer.mjs
import { readFileSync } from 'node:fs';

const read = (p) => JSON.parse(readFileSync(new URL(p, import.meta.url), 'utf8'));
const workflow = read('../workflows/ai-invoice-processor.json');
const sample = read('../workflows/sample-invoice.json');
const expected = read('../workflows/expected-extraction.json');
const validateCode = workflow.nodes.find((n) => n.name === 'Validate Totals').parameters.jsCode;

const runValidate = (items) => {
  const $input = { all: () => items.map((json) => ({ json })), first: () => ({ json: items[0] }) };
  return new Function('$input', validateCode)($input);
};

const divider = (t) => console.log(`\n${'='.repeat(68)}\n${t}\n${'='.repeat(68)}`);
const money = (n) => `$${Number(n).toFixed(2)}`;

// ---------------------------------------------------------------- SCENARIO
divider('C9 TEAMS — AI INVOICE PROCESSOR: EMPLOYER DEMO');
console.log('Company: C9 Group, Australian accounting practice (Melbourne).');
console.log('Problem: supplier invoices arrive by email and someone types them');
console.log('into the books by hand — slow, GST mistakes happen, and the same');
console.log('invoice sometimes gets paid twice.');

// ------------------------------------------------------- STEP 1: INTAKE
divider('STEP 1 — INVOICE INTAKE (webhook POST /invoice-intake)');
console.log('An invoice arrives from a supplier. The workflow receives it:');
console.log('---');
console.log(sample.text);
console.log('---');

// ------------------------------------------- STEP 2: EXTRACTION PROMPT
divider('STEP 2 — PREPARE EXTRACTION PROMPT (Code node)');
console.log('The workflow builds this prompt for Gemini (truncated):');
console.log('"Extract the invoice fields from the text below and return ONLY');
console.log(' valid JSON with this shape: {vendor, abn, invoice_number,');
console.log(' invoice_date, due_date, currency, line_items, subtotal, tax,');
console.log(' total}. Copy numbers exactly as printed; do not invent fields."');

// ------------------------------------------------- STEP 3: GEMINI EXTRACT
divider('STEP 3 — GEMINI EXTRACT (HTTP node) — SIMULATED OUTPUT');
console.log('Gemini reads the invoice and returns structured JSON.');
console.log('(Simulated here with the workflow\'s expected extraction —');
console.log(' a live call needs a Gemini API key.)');
console.log(JSON.stringify(expected, null, 2));

// -------------------------------------------------- STEP 4: VALIDATE
divider('STEP 4 — VALIDATE TOTALS (Code node — REAL code, live run)');
const result = runValidate([expected])[0].json;
console.log('valid:', result.valid, '| errors:', JSON.stringify(result.errors));
console.log('Checks the node just ran: required fields present, line items');
console.log(`sum ${money(85 + 178 + 15)} == subtotal ${money(expected.subtotal)},`);
console.log(`subtotal + tax ${money(expected.subtotal + expected.tax)} == total ${money(expected.total)}.`);

// ---------------------------------------------- STEP 5+6: VALID PATH
if (result.valid) {
  divider('STEP 5 — RECORD INVOICE (Google Sheets, "Invoices" tab)');
  console.log('Row written (invoice_number is the upsert key — a repeat');
  console.log('updates this row instead of creating a second payment):');
  console.log(
    ['vendor', 'abn', 'invoice_number', 'invoice_date', 'due_date', 'currency', 'subtotal', 'tax', 'total', 'status'].join(' | '),
  );
  console.log(
    [expected.vendor, expected.abn, expected.invoice_number, expected.invoice_date, expected.due_date, expected.currency, expected.subtotal.toFixed(2), expected.tax.toFixed(2), expected.total.toFixed(2), 'recorded'].join(' | '),
  );
  divider('STEP 6 — NOTIFY TEAM (Slack)');
  console.log('#finance — Invoice recorded ✅');
  console.log(`Acme Office Supplies Pty Ltd — INV-2026-1042 — ${money(expected.total)} AUD (GST ${money(expected.tax)}), due 2026-11-21.`);
}

// ------------------------------------------- EXCEPTION PATH (tampered)
divider('EXCEPTION PATH — SAME SUPPLIER, TAMPERED TOTAL');
const tampered = { ...expected, invoice_number: 'INV-2026-1043', total: 315.8 };
console.log('A second invoice arrives, but the total was changed on the');
console.log(`paper: $305.80 printed as $315.80. The node runs again:`);
const bad = runValidate([tampered])[0].json;
console.log('valid:', bad.valid, '| errors:', JSON.stringify(bad.errors));
divider('STEP 5b — QUARANTINE (Code node) + STEP 6b — ALERT TEAM (Slack)');
console.log('Row written to quarantine (NOT the books):');
console.log(`status: quarantined | errors: ${JSON.stringify(bad.errors)} | invoice: INV-2026-1043 | received_at: ${new Date().toISOString()}`);
console.log('\n#finance — ⚠️ Invoice needs review');
console.log('Acme Office Supplies Pty Ltd — INV-2026-1043 — total does not');
console.log('match subtotal + tax. Held in quarantine. A human checks it.');

// ------------------------------------------------------- EMPLOYER SUMMARY
divider('WHAT THE EMPLOYER GETS');
console.log('• No manual typing: every invoice is read, checked and filed');
console.log('  automatically. A person only touches the exceptions.');
console.log('• GST mistakes caught before the books: wrong totals never');
console.log('  enter silently — they wait in quarantine with a Slack alert.');
console.log('• No double payments: invoice_number is the upsert key, so a');
console.log('  repeated invoice updates one row instead of paying twice.');
console.log('• Audit trail: every invoice is a row in Sheets with a status.');
console.log('• Cost: a few cents of Gemini per invoice + n8n hosting.');
console.log('  No per-seat licence, no new software for the team.');
console.log('• Go-live: connect C9\'s inbox, Sheets (or Xero/MYOB) and');
console.log('  Slack, run it on past invoices first, measure accuracy,');
console.log('  then switch on. The team changes nothing about how they');
console.log('  receive invoices — the workflow sits behind the inbox.');
