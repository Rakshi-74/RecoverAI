from sqlalchemy import Column, String, DateTime, Text
from backend.app.database.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(String, primary_key=True)

    entity_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    actor = Column(String, nullable=False)

    decision = Column(String, nullable=True)

    details = Column(Text, nullable=True)

    created_at = Column(DateTime)