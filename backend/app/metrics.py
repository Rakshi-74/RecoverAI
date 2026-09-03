from sqlalchemy import func

from backend.app.database.database import SessionLocal
from backend.app.models.recovery import (
    RecoveryDecision,
    RecoveryAction
)


def get_recovery_metrics():

    db = SessionLocal()

    try:
        total_payments = (
            db.query(func.count(RecoveryDecision.decision_id))
            .scalar()
            or 0
        )

        revenue_at_risk = (
            db.query(func.sum(RecoveryDecision.revenue_at_risk))
            .scalar()
            or 0.0
        )

        expected_recovery = (
            db.query(
                func.sum(
                    RecoveryDecision.expected_recovery_value
                )
            )
            .scalar()
            or 0.0
        )

        approved_actions = (
            db.query(func.count(RecoveryAction.action_id))
            .filter(
                RecoveryAction.action_status.in_(
                    ["APPROVED", "SIMULATED", "CREATED"]
                )
            )
            .scalar()
            or 0
        )

        blocked_actions = (
            db.query(func.count(RecoveryAction.action_id))
            .filter(
                RecoveryAction.action_status == "BLOCKED"
            )
            .scalar()
            or 0
        )

        actual_recovered = (
            db.query(
                func.sum(
                    RecoveryAction.actual_recovered_amount
                )
            )
            .scalar()
            or 0.0
        )

        recovery_rate = 0.0

        if revenue_at_risk > 0:
            recovery_rate = (
                expected_recovery / revenue_at_risk
            ) * 100

        return {
            "total_payments": total_payments,
            "revenue_at_risk": round(
                revenue_at_risk, 2
            ),
            "expected_recovery": round(
                expected_recovery, 2
            ),
            "actual_recovered": round(
                actual_recovered, 2
            ),
            "expected_recovery_rate": round(
                recovery_rate, 2
            ),
            "approved_actions": approved_actions,
            "blocked_actions": blocked_actions
        }

    finally:
        db.close()