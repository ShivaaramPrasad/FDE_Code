from fastapi import FastAPI, HTTPException
from models import Payment, PaymentIn
from services import list_payments, get_payment, create_payment, update_payment, delete_payment

app = FastAPI()


@app.get("/payments", response_model=list[Payment])
def read_payments():
    return list_payments()


@app.get("/payments/{payment_id}", response_model=Payment)
def read_payment(payment_id: int):
    try:
        return get_payment(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/payments", response_model=Payment, status_code=201)
def create_new_payment(payment: PaymentIn):
    try:
        return create_payment(payment.model_dump())
    except LookupError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.put("/payments/{payment_id}", response_model=Payment)
def update_existing_payment(payment_id: int, updated_payment: PaymentIn):
    try:
        return update_payment(payment_id, updated_payment.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.delete("/payments/{payment_id}")
def delete_existing_payment(payment_id: int):
    try:
        delete_payment(payment_id)
        return {"detail": "Payment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
