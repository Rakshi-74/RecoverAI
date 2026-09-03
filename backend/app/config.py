import os


RAZORPAY_KEY_ID = os.getenv(
    "RAZORPAY_KEY_ID",
    "test_key_id"
)

RAZORPAY_KEY_SECRET = os.getenv(
    "RAZORPAY_KEY_SECRET",
    "test_key_secret"
)

RAZORPAY_TEST_MODE = True