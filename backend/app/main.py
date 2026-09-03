from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
import json

from backend.app.database.database import Base, engine, SessionLocal
from backend.app.models import customer
from backend.app.models import payment
from backend.app.models import recovery
from backend.app.models import audit

from ml.recovery_pipeline import run_recovery_pipeline
from backend.app.metrics import get_recovery_metrics
from backend.app.routes.webhooks import router as webhook_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="RecoverAI",
    description="Autonomous Revenue Recovery & Payment Intelligence Agent",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect webhook routes
app.include_router(webhook_router)


class PaymentRequest(BaseModel):
    payment_id: str
    amount: float
    attempt_number: int
    checkout_started: int
    checkout_duration_seconds: int
    customer_age_days: int
    lifetime_value: float
    successful_payments: int
    failed_payments: int
    previous_recoveries: int
    contact_opted_out: int
    failure_rate: float
    recovery_history_rate: float
    high_value_customer: int
    high_amount: int
    multiple_attempt: int


@app.get("/")
def root():
    return {
        "project": "RecoverAI",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/recover")
def recover_payment(payment_data: PaymentRequest):

    payment_dict = payment_data.model_dump()

    # Run complete AI recovery pipeline
    result = run_recovery_pipeline(payment_dict)

    db = SessionLocal()

    try:
        now = datetime.now()

        decision_id = str(uuid.uuid4())
        action_id = str(uuid.uuid4())
        audit_id = str(uuid.uuid4())

        expected_recovery_value = (
            result["recovery_probability"] * result["amount"]
        )

        # Get executor result
        execution = result["execution"]

        # --------------------------------
        # 1. Recovery Decision
        # --------------------------------

        decision_reason = (
            f"Recovery probability: "
            f"{result['recovery_probability'] * 100:.2f}%. "
            f"Recommended action: "
            f"{result['recommended_action']}. "
            f"Final action: "
            f"{result['final_action']}."
        )

        decision = recovery.RecoveryDecision(
            decision_id=decision_id,
            payment_id=result["payment_id"],
            recovery_probability=result["recovery_probability"],
            revenue_at_risk=result["amount"],
            expected_recovery_value=expected_recovery_value,
            recommended_action=result["recommended_action"],
            decision_reason=decision_reason,
            policy_status=result["status"],
            created_at=now
        )

        db.add(decision)

        # --------------------------------
        # 2. Recovery Action
        # --------------------------------

        action = recovery.RecoveryAction(
            action_id=action_id,
            payment_id=result["payment_id"],
            action_type=result["final_action"],
            action_status=execution["status"],
            attempt_number=payment_data.attempt_number,
            expected_value=expected_recovery_value,
            actual_recovered_amount=0.0,
            executed_at=now
        )

        db.add(action)

        # --------------------------------
        # 3. Audit Trail
        # --------------------------------

        audit_log = audit.AuditLog(
            audit_id=audit_id,
            entity_id=result["payment_id"],
            event_type="RECOVERY_EXECUTION",
            actor="RecoverAI-Agent",
            decision=result["final_action"],
            details=json.dumps({
                "recovery_probability": result[
                    "recovery_probability"
                ],
                "recommended_action": result[
                    "recommended_action"
                ],
                "final_action": result[
                    "final_action"
                ],
                "pipeline_status": result[
                    "status"
                ],
                "execution_status": execution[
                    "status"
                ],
                "execution_message": execution[
                    "message"
                ],
                "guardrail_reasons": result[
                    "guardrail_reasons"
                ],
                "expected_recovery_value":
                    expected_recovery_value
            }),
            created_at=now
        )

        db.add(audit_log)

        # Save everything
        db.commit()

        # --------------------------------
        # Final API Response
        # --------------------------------

        result["decision_id"] = decision_id
        result["database_action_id"] = action_id
        result["audit_id"] = audit_id
        result["expected_recovery_value"] = (
            expected_recovery_value
        )

        return result

    except Exception as e:

        db.rollback()

        return {
            "status": "ERROR",
            "error": str(e),
            "payment_id": payment_data.payment_id
        }

    finally:
        db.close()


# --------------------------------
# Recovery Metrics
# --------------------------------

@app.get("/api/metrics")
def recovery_metrics():
    return get_recovery_metrics()