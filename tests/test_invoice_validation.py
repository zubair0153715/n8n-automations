"""Test the same validation logic the n8n 'Validate Totals' Code node runs.

Checks against workflows/sample-invoice.json + workflows/expected-extraction.json:
1. expected extraction matches the sample invoice numbers.
2. line-items sum == subtotal, subtotal + tax == total (tolerance 0.01).
3. required fields present.
4. duplicate invoice_number is caught against a fake ledger (upsert key).

Run: python3 tests/test_invoice_validation.py  (from ~/workspace/n8n)
No network, no credentials needed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WF = os.path.join(HERE, "..", "workflows")


def load(name):
    with open(os.path.join(WF, name)) as f:
        return json.load(f)


def validate(inv, ledger_numbers):
    errors = []
    for f in ["vendor", "invoice_number", "invoice_date", "subtotal", "tax", "total"]:
        if inv.get(f) in (None, ""):
            errors.append("missing " + f)
    items = inv.get("line_items") or []
    if not items:
        errors.append("no line items")
    line_sum = sum(float(li.get("amount") or 0) for li in items)
    if abs(line_sum - float(inv.get("subtotal") or 0)) > 0.01:
        errors.append("line items sum %.2f != subtotal %s" % (line_sum, inv.get("subtotal")))
    if abs((float(inv.get("subtotal") or 0) + float(inv.get("tax") or 0)) - float(inv.get("total") or 0)) > 0.01:
        errors.append("subtotal + tax != total")
    if inv.get("invoice_number") in ledger_numbers:
        errors.append("duplicate invoice_number " + str(inv.get("invoice_number")))
    return errors


def main():
    sample = load("sample-invoice.json")
    expected = load("expected-extraction.json")
    workflow = load("ai-invoice-processor.json")
    passed = failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
            print("PASS  " + name)
        else:
            failed += 1
            print("FAIL  " + name + (" — " + detail if detail else ""))

    # 1. expected extraction matches the sample invoice text numbers
    check("sample text contains invoice number", expected["invoice_number"] in sample["text"])
    check("sample text contains total 305.80", "305.80" in sample["text"])
    check("expected subtotal == 278.00", expected["subtotal"] == 278.0)
    check("expected tax == 27.80", expected["tax"] == 27.8)
    check("expected total == 305.80", expected["total"] == 305.8)

    # 2. validation logic on the good invoice
    check("valid invoice has zero errors", validate(expected, set()) == [])

    # 3. validation catches a tampered total
    bad = dict(expected)
    bad["total"] = 999.99
    errs = validate(bad, set())
    check("tampered total is caught", len(errs) == 1 and "subtotal + tax != total" in errs, str(errs))

    # 4. validation catches a tampered line item
    bad2 = json.loads(json.dumps(expected))
    bad2["line_items"][0]["amount"] = 1.0
    errs2 = validate(bad2, set())
    check("tampered line item is caught", any("line items sum" in e for e in errs2), str(errs2))

    # 5. duplicate invoice number is caught (upsert key)
    errs3 = validate(expected, {"INV-2026-1042"})
    check("duplicate invoice_number is caught", any("duplicate" in e for e in errs3), str(errs3))

    # 6. workflow JSON structure: nodes exist, connections reference real nodes
    names = {n["name"] for n in workflow["nodes"]}
    check("workflow has 11 nodes", len(workflow["nodes"]) == 11, str(len(workflow["nodes"])))
    check("workflow has webhook trigger", any(n["type"].endswith("webhook") for n in workflow["nodes"]))
    check("workflow has error trigger", any(n["type"].endswith("errorTrigger") for n in workflow["nodes"]))
    bad_refs = []
    for src, outs in workflow["connections"].items():
        if src not in names:
            bad_refs.append("source " + src)
        for out in outs.get("main", []):
            for link in out:
                if link["node"] not in names:
                    bad_refs.append("target " + link["node"])
    check("all connections reference existing nodes", not bad_refs, ", ".join(bad_refs))
    check("no real secrets in workflow JSON",
          "YOUR_GEMINI_API_KEY" in json.dumps(workflow) and "sk-" not in json.dumps(workflow))

    print("\n%d passed, %d failed" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
