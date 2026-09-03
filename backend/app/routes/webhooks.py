from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ml.recovery_pipeline import run_recovery_pipeline

router = APIRouter()


class RazorpayWebhook(BaseModel):
    event: str
    payment_id: Optional[str] = None
    amount: Optional[float] = None


@router.post("/webhooks/razorpay")
async def razorpay_webhook(payload: RazorpayWebhook):

    if payload.event != "payment.failed":
        return {
            "status": "received",
            "event": payload.event,
            "message": "Event received but no recovery action was triggered."
        }

    if payload.payment_id is None or payload.amount is None:
        return {
            "status": "ERROR",
            "event": payload.event,
            "message": "payment_id and amount are required for recovery."
        }

    payment_data = {
        "payment_id": payload.payment_id,
        "amount": payload.amount,
        "attempt_number": 1,
        "checkout_started": 1,
        "checkout_duration_seconds": 60,
        "customer_age_days": 30,
        "lifetime_value": payload.amount,
        "successful_payments": 1,
        "failed_payments": 1,
        "previous_recoveries": 0,
        "contact_opted_out": 0,
        "failure_rate": 0.5,
        "recovery_history_rate": 0.0,
        "high_value_customer": 1 if payload.amount >= 5000 else 0,
        "high_amount": 1 if payload.amount >= 5000 else 0,
        "multiple_attempt": 0
    }

    result = run_recovery_pipeline(payment_data)

    return {
        "status": "processed",
        "event": payload.event,
        "payment_id": payload.payment_id,
        "recovery": result
    }