from ml.decision_engine import predict_recovery
from ml.guardrails import check_guardrails
from ml.action_executor import execute_action


def run_recovery_pipeline(payment):

    # 1. ML prediction + decision engine
    prediction = predict_recovery(payment)

    recovery_probability = prediction["recovery_probability"]

    # 2. Guardrails
    guardrail_result = check_guardrails(
        payment,
        recovery_probability
    )

    # 3. Decide whether execution is allowed
    if guardrail_result["allowed"]:

        final_action = prediction["recommended_action"]

        # 4. Execute approved action
        execution_result = execute_action(
            payment,
            final_action
        )

        status = "APPROVED"

    else:

        final_action = "NO_ACTION"

        execution_result = {
            "action_id": None,
            "payment_id": payment["payment_id"],
            "action": "NO_ACTION",
            "status": "BLOCKED",
            "message": "Recovery action blocked by guardrails.",
            "executed_at": None
        }

        status = "BLOCKED"

    return {
        "payment_id": prediction["payment_id"],
        "amount": prediction["amount"],
        "recovery_probability": recovery_probability,
        "recommended_action": prediction["recommended_action"],
        "final_action": final_action,
        "status": status,
        "guardrail_reasons": guardrail_result["reasons"],
        "execution": execution_result
    }


if __name__ == "__main__":

    sample_payment = {
        "payment_id": "PIPELINE_TEST_001",
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
        "failure_rate": 3 / 24,
        "recovery_history_rate": 2 / 4,
        "high_value_customer": 1,
        "high_amount": 1,
        "multiple_attempt": 0
    }

    result = run_recovery_pipeline(sample_payment)

    print("\n====================================")
    print("       RECOVERAI PIPELINE")
    print("====================================")

    print(f"Payment ID: {result['payment_id']}")
    print(f"Amount: ₹{result['amount']}")
    print(
        f"Recovery Probability: "
        f"{result['recovery_probability'] * 100:.2f}%"
    )
    print(
        f"Recommended Action: "
        f"{result['recommended_action']}"
    )
    print(
        f"Final Action: "
        f"{result['final_action']}"
    )
    print(f"Status: {result['status']}")

    print("\nExecution:")
    print(
        f"Action: "
        f"{result['execution']['action']}"
    )
    print(
        f"Execution Status: "
        f"{result['execution']['status']}"
    )
    print(
        f"Message: "
        f"{result['execution']['message']}"
    )

    print("\nGuardrail Results:")

    for reason in result["guardrail_reasons"]:
        print(f"- {reason}")