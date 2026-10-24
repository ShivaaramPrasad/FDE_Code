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
    
     {"id": 3,
          "invoice_id": "INV-0003",
          "vendor": "ABC Corp",
          "amount": 100,
          "status": "paid",
    },
]


vendor_groups = {}
for invoice in invoices:
    vendor = invoice["vendor"]
    if vendor not in vendor_groups:
        vendor_groups[vendor] = []
    vendor_groups[vendor].append(invoice)

print(vendor_groups)


vendor_totals = {}
for invoice in invoices:
    vendor = invoice["vendor"]
    amount = invoice["amount"]
    vendor_totals[vendor] = vendor_totals.get(vendor, 0) + amount

print(vendor_totals)  # Output: {'ABC Corp': 850, 'fdd Corp': 100}