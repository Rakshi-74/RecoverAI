import joblib
import pandas as pd


MODEL_PATH = "ml/recovery_model.joblib"

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
features = model_data["features"]


def calculate_action_scores(payment):
    """
    Calculate expected recovery value for each possible action.
    """

    amount = payment["amount"]
    recovery_probability = payment["recovery_probability"]

    actions = {
        "smart_retry": {
            "probability_boost": 0.10,
            "cost": 2.0
        },
        "payment_link": {
            "probability_boost": 0.15,
            "cost": 1.0
        },
        "payment_method_switch": {
            "probability_boost": 0.20,
            "cost": 1.5
        },
        "customer_reminder": {
            "probability_boost": 0.05,
            "cost": 0.5
        }
    }

    results = {}

    for action, config in actions.items():

        adjusted_probability = min(
            recovery_probability + config["probability_boost"],
            0.95
        )

        expected_value = (
            adjusted_probability * amount
        ) - config["cost"]

        results[action] = {
            "probability": round(adjusted_probability, 4),
            "expected_value": round(expected_value, 2)
        }

    return results


def predict_recovery(payment_data):
    """
    Predict recovery probability for a payment.
    """

    input_data = pd.DataFrame(
        [payment_data],
        columns=features
    )

    probability = model.predict_proba(input_data)[0][1]

    payment_data["recovery_probability"] = float(probability)

    action_scores = calculate_action_scores(payment_data)

    best_action = max(
        action_scores,
        key=lambda action: action_scores[action]["expected_value"]
    )

    return {
        "payment_id": payment_data.get("payment_id", "UNKNOWN"),
        "amount": payment_data["amount"],
        "recovery_probability": round(float(probability), 4),
        "recommended_action": best_action,
        "action_scores": action_scores
    }


if __name__ == "__main__":

    sample_payment = {
        "payment_id": "TEST_001",
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

    result = predict_recovery(sample_payment)

    print("\n====================================")
    print("        RECOVERAI DECISION ENGINE")
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

    print("\nAction Analysis:")

    for action, score in result["action_scores"].items():
        print(
            f"{action}: "
            f"Probability={score['probability'] * 100:.2f}% | "
            f"Expected Value=₹{score['expected_value']:.2f}"
        )