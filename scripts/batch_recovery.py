import json

from ml.recovery_pipeline import run_recovery_pipeline


def simulate_batch(payments):

    results = []

    total_revenue_at_risk = 0.0
    total_expected_recovery = 0.0
    approved_count = 0
    blocked_count = 0

    for payment in payments:

        result = run_recovery_pipeline(payment)

        expected_recovery = (
            result["recovery_probability"]
            * result["amount"]
        )

        total_revenue_at_risk += result["amount"]
        total_expected_recovery += expected_recovery

        if result["status"] == "APPROVED":
            approved_count += 1
        else:
            blocked_count += 1

        results.append({
            "payment_id": result["payment_id"],
            "amount": result["amount"],
            "recovery_probability": result["recovery_probability"],
            "recommended_action": result["recommended_action"],
            "final_action": result["final_action"],
            "status": result["status"],
            "expected_recovery_value": expected_recovery
        })

    return {
        "total_payments": len(payments),
        "total_revenue_at_risk": total_revenue_at_risk,
        "total_expected_recovery": total_expected_recovery,
        "approved_actions": approved_count,
        "blocked_actions": blocked_count,
        "results": results
    }


if __name__ == "__main__":

    payments = [
        {
            "payment_id": "BATCH_001",
            "amount": 5000,
            "attempt_number": 1,
            "checkout_started": 1,
            "checkout_duration_seconds": 45,
            "customer_age_days": 500,
            "lifetime_value": 75000,
            "successful_payments": 20,
            "failed_payments": 3,
            "previous_recoveries": 2,
            "contact_opted_out": 0,
            "failure_rate": 0.125,
            "recovery_history_rate": 0.5,
            "high_value_customer": 1,
            "high_amount": 1,
            "multiple_attempt": 0
        },
        {
            "payment_id": "BATCH_002",
            "amount": 2500,
            "attempt_number": 1,
            "checkout_started": 1,
            "checkout_duration_seconds": 30,
            "customer_age_days": 200,
            "lifetime_value": 30000,
            "successful_payments": 10,
            "failed_payments": 2,
            "previous_recoveries": 1,
            "contact_opted_out": 0,
            "failure_rate": 0.1538,
            "recovery_history_rate": 0.3333,
            "high_value_customer": 0,
            "high_amount": 0,
            "multiple_attempt": 0
        },
        {
            "payment_id": "BATCH_003",
            "amount": 10000,
            "attempt_number": 3,
            "checkout_started": 1,
            "checkout_duration_seconds": 60,
            "customer_age_days": 900,
            "lifetime_value": 120000,
            "successful_payments": 40,
            "failed_payments": 5,
            "previous_recoveries": 3,
            "contact_opted_out": 0,
            "failure_rate": 0.1087,
            "recovery_history_rate": 0.5,
            "high_value_customer": 1,
            "high_amount": 1,
            "multiple_attempt": 1
        },
        {
            "payment_id": "BATCH_004",
            "amount": 1500,
            "attempt_number": 1,
            "checkout_started": 0,
            "checkout_duration_seconds": 10,
            "customer_age_days": 50,
            "lifetime_value": 5000,
            "successful_payments": 2,
            "failed_payments": 5,
            "previous_recoveries": 0,
            "contact_opted_out": 1,
            "failure_rate": 0.625,
            "recovery_history_rate": 0.0,
            "high_value_customer": 0,
            "high_amount": 0,
            "multiple_attempt": 0
        }
    ]

    result = simulate_batch(payments)

    print("\n====================================")
    print("      RECOVERAI BATCH SIMULATOR")
    print("====================================")

    print(
        f"Total Payments: "
        f"{result['total_payments']}"
    )

    print(
        f"Revenue at Risk: "
        f"₹{result['total_revenue_at_risk']:.2f}"
    )

    print(
        f"Expected Recovery: "
        f"₹{result['total_expected_recovery']:.2f}"
    )

    print(
        f"Approved Actions: "
        f"{result['approved_actions']}"
    )

    print(
        f"Blocked Actions: "
        f"{result['blocked_actions']}"
    )

    print("\nPayment Results:")

    for item in result["results"]:

        print(
            f"\n{item['payment_id']}"
        )

        print(
            f"Amount: ₹{item['amount']:.2f}"
        )

        print(
            f"Recovery Probability: "
            f"{item['recovery_probability'] * 100:.2f}%"
        )

        print(
            f"Action: "
            f"{item['final_action']}"
        )

        print(
            f"Status: "
            f"{item['status']}"
        )

        print(
            f"Expected Recovery: "
            f"₹{item['expected_recovery_value']:.2f}"
        )