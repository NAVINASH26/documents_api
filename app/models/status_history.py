
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
import uuid

class DocumentStatusHistory(Base):
    __tablename__ = "document_status_history"

    id = Column(String(36), primary_key=True, index=True,default=lambda:str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"))
    status = Column(String(20))
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    document = relationship("Document", back_populates="status_history")