import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "invoices.json"

with open(DATA_FILE, encoding="utf-8") as f:
    invoices = json.load(f)


# Exercise 1: total amount by vendor
vendor_totals = {}
for invoice in invoices:
    vendor = invoice["vendor"]
    vendor_totals[vendor] = vendor_totals.get(vendor, 0) + invoice["amount"]

print("Totals by vendor:")
for vendor, total in vendor_totals.items():
    print(f"  {vendor}: {total}")


# Exercise 2: invoices whose vendor appears more than once
vendor_counts = {}
for invoice in invoices:
    vendor_counts[invoice["vendor"]] = vendor_counts.get(invoice["vendor"], 0) + 1

duplicates = [inv for inv in invoices if vendor_counts[inv["vendor"]] > 1]

print("Duplicate vendor invoices:")
for invoice in duplicates:
    print(f"  {invoice}")
