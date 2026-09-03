from datetime import datetime
import uuid

from backend.app.services.razorpay_client import create_payment_link


def execute_action(payment, action):

    payment_id = payment["payment_id"]
    amount = payment["amount"]

    action_id = str(uuid.uuid4())
    executed_at = datetime.now().isoformat()

    if action == "payment_link":

        razorpay_result = create_payment_link(
            amount=amount,
            description="RecoverAI payment recovery",
            reference_id=payment_id
        )

        return {
            "action_id": action_id,
            "payment_id": payment_id,
            "action": action,
            "status": razorpay_result["status"],
            "message": razorpay_result["message"],
            "payment_link": razorpay_result.get("payment_link"),
            "payment_link_id": razorpay_result.get("payment_link_id"),
            "executed_at": executed_at
        }

    elif action == "smart_retry":

        return {
            "action_id": action_id,
            "payment_id": payment_id,
            "action": action,
            "status": "SIMULATED",
            "message": (
                f"Smart payment retry initiated "
                f"for payment {payment_id}"
            ),
            "payment_link": None,
            "payment_link_id": None,
            "executed_at": executed_at
        }

    elif action == "payment_method_switch":

        return {
            "action_id": action_id,
            "payment_id": payment_id,
            "action": action,
            "status": "SIMULATED",
            "message": (
                f"Payment method switch recommended "
                f"for payment {payment_id}"
            ),
            "payment_link": None,
            "payment_link_id": None,
            "executed_at": executed_at
        }

    elif action == "customer_reminder":

        return {
            "action_id": action_id,
            "payment_id": payment_id,
            "action": action,
            "status": "SIMULATED",
            "message": (
                f"Customer reminder scheduled "
                f"for payment {payment_id}"
            ),
            "payment_link": None,
            "payment_link_id": None,
            "executed_at": executed_at
        }

    else:

        return {
            "action_id": action_id,
            "payment_id": payment_id,
            "action": action,
            "status": "BLOCKED",
            "message": "Unknown recovery action. Execution blocked.",
            "payment_link": None,
            "payment_link_id": None,
            "executed_at": executed_at
        }


if __name__ == "__main__":

    test_payment = {
        "payment_id": "TEST_001",
        "amount": 5000
    }

    result = execute_action(
        test_payment,
        "payment_link"
    )

    print("\n====================================")
    print("      RECOVERAI ACTION EXECUTOR")
    print("====================================")
    print(f"Payment ID: {result['payment_id']}")
    print(f"Action: {result['action']}")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Payment Link: {result['payment_link']}")
    print(f"Action ID: {result['action_id']}")
    print(f"Executed At: {result['executed_at']}")