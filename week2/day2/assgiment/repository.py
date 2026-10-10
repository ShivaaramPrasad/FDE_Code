import json
from pathlib import Path

# payments.json holds {"invoices": [...], "payments": [...]}, related through invoice_id
DATA_FILE = Path(__file__).with_name("payments.json")


def _load_all():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["invoices"], data["payments"]


def _save_all(invoices, payments):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"invoices": invoices, "payments": payments}, f, indent=4)


def load_invoices():
    return _load_all()[0]


def load_payments():
    return _load_all()[1]


def find_invoice_by_id(invoice_id):
    return next((inv for inv in load_invoices() if inv["invoice_id"] == invoice_id), None)


def find_payment_by_id(payment_id):
    return next((p for p in load_payments() if p["payment_id"] == payment_id), None)


def next_payment_id():
    return max((p["payment_id"] for p in load_payments()), default=0) + 1


def add_payment(payment):
    invoices, payments = _load_all()
    payments.append(payment)
    _save_all(invoices, payments)


def update_payment(payment_id, updated_payment):
    invoices, payments = _load_all()
    for index, payment in enumerate(payments):
        if payment["payment_id"] == payment_id:
            payments[index] = updated_payment
            _save_all(invoices, payments)
            return True
    return False


def delete_payment(payment_id):
    invoices, payments = _load_all()
    for index, payment in enumerate(payments):
        if payment["payment_id"] == payment_id:
            del payments[index]
            _save_all(invoices, payments)
            return True
    return False
