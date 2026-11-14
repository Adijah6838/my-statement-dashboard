from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # The owner of the record
    transaction_type = Column(String, nullable=False) # deposit, withdrawal, transfer
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    sender_name = Column(String, nullable=True)
    receiver_name = Column(String, nullable=True)
    status = Column(String, default="completed")