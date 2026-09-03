from sqlalchemy import Column, String, Integer, Float, Boolean
from backend.app.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)

    customer_age_days = Column(Integer, default=0)

    lifetime_value = Column(Float, default=0.0)

    successful_payments = Column(Integer, default=0)

    failed_payments = Column(Integer, default=0)

    previous_recoveries = Column(Integer, default=0)

    contact_opted_out = Column(Boolean, default=False)