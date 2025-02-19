from sqlalchemy import String, Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship 
from .database import Base
from datetime import datetime
import secrets




# random id
def random_id():
    return secrets.token_hex(16)


def generate_ref():
    return secrets.token_hex(16)


def generate_session_id():
    return secrets.token_hex(16)


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=random_id)
    username = Column(String)
    email = Column(String)
    account_number = Column(String)
    phone = Column(String)
    password = Column(String)
    is_active = Column(String,  default=True)
    is_admin = Column(String,  default=False)
    wallet_balance = Column(Float, default=0)
    book_balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bvn = Column(Integer, nullable=True)
    nin = Column(Integer, nullable=True)
    level_1 = Column(String, default=True)
    level_2 = Column(String, default=False)
    level_3 = Column(String, default=False)
    transaction_pin = Column(String)
    transaction_limit_per_transaction = Column(Float, default=20000.0)
    transaction_limit_per_day = Column(Float, default=50000.0)
    locked_funds = relationship("LockedFunds", back_populates="user", cascade="all, delete")
    
    
    
class LockedFunds(Base):
    __tablename__ = "locked_funds"
    id = Column(String, primary_key=True, default=random_id)
    user_id = Column(String, ForeignKey("users.id"))
    amount = Column(Float, default=0.0)
    release_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="locked_funds")
    
    
    
    
class Transfers(Base):
    __tablename__ = "transfers"
    
    id = Column(String, primary_key=True, default=random_id)
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date_sent = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String, nullable=False)
    transaction_ref = Column(String, nullable=False, default=generate_ref)
    session_id = Column(String, nullable=False, default=generate_session_id)
    status = Column(String, nullable=False, default="pending") 

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    def __init__(self, sender_id, receiver_id, amount, date_sent=None, status="pending"):
        self.id = random_id()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        # self.receiver_name = receiver.username
        self.amount = f"{amount:.2f}"
        self.date_sent = date_sent or datetime.utcnow()
        self.transaction_type = "debit" if sender_id else "credit"
        self.status = status
