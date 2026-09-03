from sqlalchemy import Column, String, Float, Integer, DateTime
from backend.app.database.database import Base


class RecoveryDecision(Base):
    __tablename__ = "recovery_decisions"

    decision_id = Column(String, primary_key=True)

    payment_id = Column(String, nullable=False)

    recovery_probability = Column(Float, nullable=False)

    revenue_at_risk = Column(Float, nullable=False)

    expected_recovery_value = Column(Float, nullable=False)

    recommended_action = Column(String, nullable=False)

    decision_reason = Column(String, nullable=False)

    policy_status = Column(String, nullable=False)

    created_at = Column(DateTime)


class RecoveryAction(Base):
    __tablename__ = "recovery_actions"

    action_id = Column(String, primary_key=True)

    payment_id = Column(String, nullable=False)

    action_type = Column(String, nullable=False)

    action_status = Column(String, nullable=False)

    attempt_number = Column(Integer, default=1)

    expected_value = Column(Float, default=0.0)

    actual_recovered_amount = Column(Float, default=0.0)

    executed_at = Column(DateTime)