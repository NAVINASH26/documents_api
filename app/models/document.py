
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    uploaded_by = Column(Integer, ForeignKey("users.id"))

    # Relationship
    owner = relationship("User", back_populates="documents")
    status_history = relationship("DocumentStatusHistory", back_populates="document")