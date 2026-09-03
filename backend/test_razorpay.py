from backend.app.services.razorpay_client import create_payment_link


result = create_payment_link(
    amount=5000,
    description="RecoverAI payment recovery",
    reference_id="TEST_001"
)

print("\n====================================")
print("      RAZORPAY CLIENT TEST")
print("====================================")

print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print(f"Reference ID: {result['reference_id']}")
print(f"Payment Link: {result['payment_link']}")