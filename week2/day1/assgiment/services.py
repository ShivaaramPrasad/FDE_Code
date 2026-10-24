import repository
from models import Payment


def list_payments() -> list[Payment]:
    return [Payment(**p) for p in repository.load_payments()]


def get_payment(payment_id: int) -> Payment:
    payment_data = repository.find_payment_by_id(payment_id)
    if payment_data is None:
        raise ValueError(f"Payment with ID {payment_id} not found.")
    return Payment(**payment_data)


def _check_invoice_exists(invoice_id: str) -> None:
    if repository.find_invoice_by_id(invoice_id) is None:
        raise LookupError(f"Invoice {invoice_id} not found.")


def create_payment(payment_data: dict) -> Payment:
    _check_invoice_exists(payment_data["invoice_id"])
    new_payment = Payment(payment_id=repository.next_payment_id(), **payment_data)
    repository.add_payment(new_payment.model_dump())
    return new_payment


def update_payment(payment_id: int, updated_data: dict) -> Payment:
    existing_payment = repository.find_payment_by_id(payment_id)
    if existing_payment is None:
        raise ValueError(f"Payment with ID {payment_id} not found.")
    _check_invoice_exists(updated_data["invoice_id"])

    updated_payment = Payment(payment_id=payment_id, **updated_data)
    repository.update_payment(payment_id, updated_payment.model_dump())
    return updated_payment


def delete_payment(payment_id: int) -> None:
    if repository.find_payment_by_id(payment_id) is None:
        raise ValueError(f"Payment with ID {payment_id} not found.")
    repository.delete_payment(payment_id)
