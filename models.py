from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    __tablename__ = "students"

    phone_number = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    opt_in_status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)  # The 'wamid' from Meta
    phone_number = Column(String, ForeignKey("students.phone_number"))
    message_text = Column(String)
    direction = Column(String)  # "inbound" or "outbound"
    status = Column(String, default="sent")  # sent, delivered, read, failed
    error_message = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())