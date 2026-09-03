import os
import razorpay

from backend.app.config import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET
)


def get_razorpay_client():

    key_id = os.getenv(
        "RAZORPAY_KEY_ID",
        RAZORPAY_KEY_ID
    )

    key_secret = os.getenv(
        "RAZORPAY_KEY_SECRET",
        RAZORPAY_KEY_SECRET
    )

    if (
        key_id == "test_key_id"
        or key_secret == "test_key_secret"
    ):
        return None

    return razorpay.Client(
        auth=(key_id, key_secret)
    )


def create_payment_link(
    amount,
    description,
    reference_id
):

    client = get_razorpay_client()

    if client is None:
        return {
            "status": "SIMULATED",
            "message": "Razorpay Test Mode credentials not configured.",
            "payment_link": None,
            "reference_id": reference_id
        }

    data = {
        "amount": int(amount * 100),
        "currency": "INR",
        "description": description,
        "reference_id": reference_id,
        "callback_method": "get"
    }

    payment_link = client.payment_link.create(data)

    return {
        "status": "CREATED",
        "message": "Razorpay payment link created successfully.",
        "payment_link": payment_link.get("short_url"),
        "payment_link_id": payment_link.get("id"),
        "reference_id": reference_id
    }