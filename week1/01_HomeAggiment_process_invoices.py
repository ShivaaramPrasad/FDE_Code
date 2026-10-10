import csv
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "data" / "homework_invoices.csv"
OUTPUT_FILE = BASE_DIR / "data" / "high_value_invoices.csv"
THRESHOLD = 100_000


def parse_amount(raw):
    """Return the amount as a float, or None if missing/invalid."""
    if raw is None:
        return None
    cleaned = raw.strip().replace(",", "").replace("₹", "")
    if not cleaned:
        return None
    try:
        value = float(cleaned)
    except ValueError:
        return None
    return value if value >= 0 else None


def main():
    high_value = []
    skipped = []
    vendor_totals = defaultdict(float)

    with open(INPUT_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            amount = parse_amount(row.get("amount"))
            if amount is None:
                skipped.append(row)
                continue

            vendor = (row.get("vendor") or "").strip() or "UNKNOWN"
            if amount > THRESHOLD:
                high_value.append(row)
                vendor_totals[vendor] += amount

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(high_value)

    print(f"Invoices above ₹{THRESHOLD:,}: {len(high_value)} -> {OUTPUT_FILE.name}")
    print(f"Skipped (missing/invalid amount): {len(skipped)}")
    for row in skipped:
        print(f"  {row['invoice_id']}: amount={row['amount']!r}")

    print("\nHigh-value totals by vendor:")
    for vendor, total in sorted(vendor_totals.items(), key=lambda kv: -kv[1]):
        print(f"  {vendor:<20} ₹{total:>12,.2f}")


if __name__ == "__main__":
    main()
