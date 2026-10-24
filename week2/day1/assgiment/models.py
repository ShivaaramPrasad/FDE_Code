from pydantic import BaseModel


class PaymentIn(BaseModel):
    invoice_id: str
    paid: float


class Payment(PaymentIn):
    payment_id: int
