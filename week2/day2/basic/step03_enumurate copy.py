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


for index, invoice in enumerate(invoices):
    if invoice["id"] == 2:
        invoices[index]["invoice_id"] = "INV-002"
    print(index, invoice)
