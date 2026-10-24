import repository

# invoices and payments both come from payments.json and are joined on invoice_id
invoices = repository.load_invoices()
payments = repository.load_payments()

# original row number of every invoice, kept in step with removals so that
# every report below refers to the row numbers of the source file
row_of = list(range(len(invoices)))


# Task 1: normalize in place, report rows with no amount
for index in range(len(invoices)):
    invoices[index]["vendor"] = invoices[index]["vendor"].strip().title()
    invoices[index]["status"] = invoices[index]["status"].upper()

print("Task 1: missing amounts")
for index, invoice in enumerate(invoices):
    if invoice["amount"] is None:
        print(f"  row {row_of[index]}: {invoice['invoice_id']} has no amount (excluded from totals)")


# Task 2: exact duplicates
seen = {}
for index, invoice in enumerate(invoices):
    key = tuple(sorted(invoice.items()))
    seen.setdefault(key, []).append(index)

exact_dupes = {key: indexes for key, indexes in seen.items() if len(indexes) > 1}

# keep the first row of each group; delete from the back so earlier indexes stay valid
to_remove = sorted((i for indexes in exact_dupes.values() for i in indexes[1:]), reverse=True)

print("Task 2: exact duplicates")
for key, indexes in exact_dupes.items():
    print(f"  {dict(key)['invoice_id']}: rows {[row_of[i] for i in indexes]}, keeping row {row_of[indexes[0]]}")
for index in to_remove:
    del invoices[index]
    del row_of[index]


# Task 3: suspected duplicates (same vendor, amount, date, different id)
print("Task 3: suspected duplicates")
for j in range(len(invoices)):
    for i in range(j):
        a, b = invoices[i], invoices[j]
        if a["amount"] is None or a["invoice_id"] == b["invoice_id"]:
            continue
        if (a["vendor"], a["amount"], a["date"]) == (b["vendor"], b["amount"], b["date"]):
            print(f"  ({b['invoice_id']} ~ {a['invoice_id']})")


# Task 4: credit notes
print("Task 4: credit notes")
for index, credit in enumerate(invoices):
    if credit["amount"] is None or credit["amount"] >= 0 or credit["status"] == "CANCELLED":
        continue

    candidates = [
        i for i, inv in enumerate(invoices)
        if inv["amount"] is not None
        and inv["amount"] == -credit["amount"]
        and inv["vendor"] == credit["vendor"]
        and inv["status"] != "CANCELLED"
    ]
    if not candidates:
        print(f"  row {row_of[index]}: credit note {credit['invoice_id']} has no partner")
        continue

    # prefer a positive invoice that comes before the credit note
    earlier = [i for i in candidates if i < index]
    partner = (earlier or candidates)[0]
    credit["status"] = "CANCELLED"
    invoices[partner]["status"] = "CANCELLED"
    print(f"  {row_of[index]} <-> {row_of[partner]}")


# Task 5: reconcile payments against invoices
active = [inv for inv in invoices if inv["amount"] is not None and inv["status"] != "CANCELLED"]

print("Vendor totals (excluding cancelled and missing amounts)")
vendor_totals = {}
for invoice in active:
    vendor_totals[invoice["vendor"]] = vendor_totals.get(invoice["vendor"], 0) + invoice["amount"]
for vendor, total in vendor_totals.items():
    print(f"  {vendor}: {total:,.0f}")

paid_by_invoice = {}
for payment in payments:
    paid_by_invoice[payment["invoice_id"]] = paid_by_invoice.get(payment["invoice_id"], 0) + payment["paid"]

billed_by_invoice = {}
for invoice in active:
    billed_by_invoice[invoice["invoice_id"]] = billed_by_invoice.get(invoice["invoice_id"], 0) + invoice["amount"]

print("Task 5: payment reconciliation")
print(f"  {'invoice':<10} {'billed':>10} {'paid':>10} {'balance':>10}  result")
for invoice_id, billed in billed_by_invoice.items():
    paid = paid_by_invoice.get(invoice_id, 0)
    balance = billed - paid
    if paid == 0:
        result = "UNPAID"
    elif balance > 0:
        result = "PARTIALLY PAID"
    elif balance < 0:
        result = "OVERPAID"
    else:
        result = "PAID"
    print(f"  {invoice_id:<10} {billed:>10,.0f} {paid:>10,.0f} {balance:>10,.0f}  {result}")

print("Payments with no matching invoice")
for invoice_id, paid in paid_by_invoice.items():
    if invoice_id not in billed_by_invoice:
        print(f"  {invoice_id}: {paid:,.0f}")
