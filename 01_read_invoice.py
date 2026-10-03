"""Read invoice records from a CSV file and report on their amounts.

Flow:
    Read CSV -> Read each invoice -> Check amount -> Handle invalid data -> Print summary

For every invoice the program reads the vendor, amount and status, then:
    * flags invoices whose amount is greater than a threshold (default 100,000)
    * flags invoices whose amount is missing or invalid (blank, "TBD", negative, ...)

Invalid amounts are handled with try/except, so one bad row never stops the
processing of the remaining records.

Usage:
    python 01_read_invoice.py
    python 01_read_invoice.py --file data/homework_invoices.csv --threshold 200000
    python 01_read_invoice.py --output data/high_value_invoices.csv

Expected CSV columns:
    invoice_id, vendor, amount, status
"""

import argparse
import csv
import logging
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

DEFAULT_FILE = Path(__file__).parent / "data" / "homework_invoices.csv"
DEFAULT_THRESHOLD = 100_000
REQUIRED_COLUMNS = {"invoice_id", "vendor", "amount", "status"}
UNKNOWN_VENDOR = "UNKNOWN"

logger = logging.getLogger(__name__)


@dataclass
class Invoice:
    """A single invoice row after it has been read and checked.

    Attributes:
        invoice_id: Identifier from the CSV (e.g. "INV-2001").
        vendor: Vendor name, or UNKNOWN_VENDOR if the cell was blank.
        status: Invoice status such as PENDING or APPROVED.
        raw_amount: The amount text exactly as it appeared in the CSV.
        amount: The parsed amount, or None if it was missing/invalid.
        error: Why the amount was rejected, or None if it was valid.
    """

    invoice_id: str
    vendor: str
    status: str
    raw_amount: str
    amount: Optional[float] = None
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """True when the amount was parsed successfully."""
        return self.amount is not None

    def is_above(self, threshold: float) -> bool:
        """True when the amount is valid and strictly greater than threshold."""
        return self.amount is not None and self.amount > threshold


def parse_amount(raw: str) -> float:
    """Convert raw amount text to a non-negative float.

    Thousands separators and the rupee sign are ignored.

    Args:
        raw: Amount text from the CSV, e.g. "142500" or "₹1,00,000".

    Returns:
        The amount as a float.

    Raises:
        ValueError: If the text is empty, not a number, not finite, or negative.
    """
    cleaned = raw.strip().replace(",", "").replace("₹", "")
    if not cleaned:
        raise ValueError("amount is missing")
    try:
        value = float(cleaned)
    except ValueError:
        raise ValueError(f"amount is not a number: {raw!r}") from None
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"amount is not a finite number: {raw!r}")
    if value < 0:
        raise ValueError(f"amount is negative: {raw!r}")
    return value


def read_invoices(path: Path) -> Iterator[Invoice]:
    """Read a CSV file and yield one checked Invoice per row.

    Rows with an invalid amount are still yielded (with `error` set) so the
    caller can count and report them while processing continues.

    Args:
        path: Location of the invoice CSV.

    Yields:
        Invoice objects, in file order.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the CSV is missing required columns.
    """
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

        for row in reader:
            raw_amount = (row.get("amount") or "").strip()
            invoice = Invoice(
                invoice_id=(row.get("invoice_id") or "").strip(),
                vendor=(row.get("vendor") or "").strip() or UNKNOWN_VENDOR,
                status=(row.get("status") or "").strip().upper(),
                raw_amount=raw_amount,
            )
            try:
                invoice.amount = parse_amount(raw_amount)
            except ValueError as exc:
                # Record the problem and carry on with the next record.
                invoice.error = str(exc)
                logger.warning("%s: %s", invoice.invoice_id, exc)
            yield invoice


def write_high_value(invoices: list[Invoice], path: Path) -> None:
    """Write the high-value invoices to a new CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["invoice_id", "vendor", "amount", "status"])
        for inv in invoices:
            writer.writerow([inv.invoice_id, inv.vendor, inv.raw_amount, inv.status])


def print_summary(invoices: list[Invoice], threshold: float) -> None:
    """Print the summary required by the assignment, plus extra breakdowns."""
    high_value = [i for i in invoices if i.is_above(threshold)]
    invalid = [i for i in invoices if not i.is_valid]

    print("\n--- Summary ---")
    print(f"Total invoices read: {len(invoices)}")
    print(f"Invoices greater than {threshold:,.0f}: {len(high_value)}")
    print(f"Invoices with missing/invalid amount: {len(invalid)}")

    if invalid:
        print("\nInvalid invoices:")
        for inv in invalid:
            print(f"  {inv.invoice_id:<10} {inv.error}")

    status_counts = Counter(i.status or "N/A" for i in invoices)
    print("\nInvoices by status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status:<10} {count}")

    vendor_totals: dict[str, float] = defaultdict(float)
    for inv in high_value:
        vendor_totals[inv.vendor] += inv.amount
    if vendor_totals:
        print(f"\nHigh-value totals by vendor (> {threshold:,.0f}):")
        for vendor, total in sorted(vendor_totals.items(), key=lambda kv: -kv[1]):
            print(f"  {vendor:<20} {total:>14,.2f}")


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Read an invoice CSV and summarise amounts.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="input CSV path")
    parser.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help="flag invoices with amount greater than this (default: %(default)s)",
    )
    parser.add_argument("--output", type=Path, help="optional CSV to write high-value invoices to")
    parser.add_argument("-v", "--verbose", action="store_true", help="show warnings for invalid rows")
    return parser.parse_args()


def main() -> int:
    """Run the program. Returns a process exit code (0 on success)."""
    args = parse_args()
    logging.basicConfig(
        level=logging.WARNING if args.verbose else logging.ERROR,
        format="%(levelname)s: %(message)s",
    )

    try:
        invoices = list(read_invoices(args.file))
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    for inv in invoices:
        if inv.is_above(args.threshold):
            print(f"{inv.invoice_id:<10} {inv.vendor:<20} {inv.status:<9} {inv.amount:>12,.2f}  > {args.threshold:,.0f}")
        elif not inv.is_valid:
            print(f"{inv.invoice_id:<10} {inv.vendor:<20} {inv.status:<9} INVALID ({inv.error})")

    print_summary(invoices, args.threshold)

    if args.output:
        write_high_value([i for i in invoices if i.is_above(args.threshold)], args.output)
        print(f"\nHigh-value invoices written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
