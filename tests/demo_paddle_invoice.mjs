// Live demo: run the AI Invoice Processor's REAL "Validate Totals" node code
// (extracted verbatim from workflows/ai-invoice-processor.json) against the
// real Paddle invoice email (136531-10002, $53.35) plus tampered variants.
// Usage: node tests/demo_paddle_invoice.mjs
import { readFileSync } from 'node:fs';

const workflow = JSON.parse(readFileSync(new URL('../workflows/ai-invoice-processor.json', import.meta.url), 'utf8'));
const node = workflow.nodes.find((n) => n.name === 'Validate Totals');
const jsCode = node.parameters.jsCode;

// Minimal $input shim matching n8n's Code-node API
const runNode = (items) => {
  const $input = { all: () => items.map((json) => ({ json })), first: () => ({ json: items[0] }) };
  return new Function('$input', jsCode)($input);
};

const paddleInvoice = {
  vendor: 'Paddle.com Inc',
  invoice_number: '136531-10002',
  invoice_date: '2026-11-09',
  currency: 'USD',
  line_items: [{ description: 'PharmaReg AI Professional', qty: 1, unit_price: 49.0, amount: 49.0 }],
  subtotal: 49.0,
  tax: 4.35,
  total: 53.35,
};

const show = (label, result) => {
  const r = result[0].json;
  const path = r.valid ? 'Record Invoice (Sheets) + Notify Team (Slack)' : 'Quarantine + Alert Team (Slack)';
  console.log(`\n--- ${label} ---`);
  console.log('valid:', r.valid, '| errors:', JSON.stringify(r.errors));
  console.log('-> path:', path);
};

// Case 1: the real Paddle invoice, exactly as printed
show('CASE 1 — Real Paddle invoice 136531-10002 ($53.35)', runNode([paddleInvoice]));

// Case 2: same invoice, total tampered $53.35 -> $54.35
show(
  'CASE 2 — Tampered total ($54.35 instead of $53.35)',
  runNode([{ ...paddleInvoice, total: 54.35 }]),
);

// Case 3: line-item amount tampered $49.00 -> $48.00
show(
  'CASE 3 — Tampered line item ($48.00 instead of $49.00)',
  runNode([{ ...paddleInvoice, line_items: [{ ...paddleInvoice.line_items[0], amount: 48.0 }] }]),
);

// Case 4: duplicate — same invoice_number arrives a second time.
// The Record Invoice (Sheets) node matches on invoice_number with
// appendOrUpdate, so a repeat updates the existing row instead of
// creating a second payment row.
const seen = new Set();
const arrive = (inv) => {
  if (seen.has(inv.invoice_number)) return `DUPLICATE ${inv.invoice_number} — update existing row, NO second payment`;
  seen.add(inv.invoice_number);
  return `NEW ${inv.invoice_number} — record row`;
};
console.log('\n--- CASE 4 — Duplicate invoice_number ---');
console.log('1st arrival :', arrive(paddleInvoice));
console.log('2nd arrival :', arrive(paddleInvoice));
