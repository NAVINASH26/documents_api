
from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String(100), primary_key=True, index=True,default=lambda:str(uuid.uuid4()))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")

    documents = relationship("Document", back_populates="owner")