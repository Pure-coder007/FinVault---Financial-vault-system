from sqlalchemy import String, Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship 
from .database import Base
from datetime import datetime



# random id
def random_id():
    import secrets
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
    sender_id = Column(String, ForeignKey("users.id"))
    receiver_id = Column(String, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    
  