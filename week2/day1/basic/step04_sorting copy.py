invoices = [
    {"id": 1,
     "invoice_id": "INV-001",
     "vendor": "ABC Corp",
     "amount": 750,
     "status": "pending",
     },
    {"id": 2,
     "invoice_id": "INV-0002",
     "vendor": "fdd Corp",
     "amount": 100,
     "status": "paid",
     },
]


sorted_invoices = sorted(invoices, key=lambda invoice: invoice["amount"], reverse=True)
print(sorted_invoices)
print(sorted_invoices[0]["amount"])