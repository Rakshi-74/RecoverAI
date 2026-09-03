from sqlalchemy import Column, String, Float, Integer, DateTime
from backend.app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False)
    failure_reason = Column(String, nullable=True)
    attempt_number = Column(Integer, default=1)
    checkout_started = Column(Integer, default=0)
    checkout_duration_seconds = Column(Integer, default=0)
    created_at = Column(DateTime)
    