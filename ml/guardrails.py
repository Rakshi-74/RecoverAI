from datetime import datetime, timedelta


MAX_ATTEMPTS = 3
MIN_RECOVERY_PROBABILITY = 0.30
COOLDOWN_MINUTES = 30


def check_guardrails(payment, recovery_probability):
    """
    Check whether RecoverAI is allowed to execute
    a recovery action.
    """

    reasons = []
    allowed = True

    # 1. Customer opted out
    if payment.get("contact_opted_out", 0) == 1:
        allowed = False
        reasons.append("Customer has opted out of contact.")

    # 2. Too many payment attempts
    if payment.get("attempt_number", 1) >= MAX_ATTEMPTS:
        allowed = False
        reasons.append("Maximum payment attempts reached.")

    # 3. Recovery probability too low
    if recovery_probability < MIN_RECOVERY_PROBABILITY:
        allowed = False
        reasons.append("Recovery probability is too low.")

    # 4. Cooldown check
    last_action = payment.get("last_action_time")

    if last_action:
        try:
            last_action_time = datetime.fromisoformat(last_action)
            time_since_action = datetime.now() - last_action_time

            if time_since_action < timedelta(minutes=COOLDOWN_MINUTES):
                allowed = False
                reasons.append("Recovery action is still within cooldown period.")

        except ValueError:
            reasons.append("Invalid last action timestamp.")

    if allowed:
        reasons.append("All guardrails passed.")

    return {
        "allowed": allowed,
        "reasons": reasons
    }


if __name__ == "__main__":

    test_payment = {
        "payment_id": "TEST_001",
        "amount": 5000,
        "attempt_number": 1,
        "contact_opted_out": 0
    }

    recovery_probability = 0.9143

    result = check_guardrails(
        test_payment,
        recovery_probability
    )

    print("\n====================================")
    print("        RECOVERAI GUARDRAILS")
    print("====================================")

    print(f"Allowed: {result['allowed']}")

    print("\nGuardrail Results:")

    for reason in result["reasons"]:
        print(f"- {reason}")