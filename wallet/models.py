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
    locked_funds = Column(Float, default=0)
    transaction_pin = Column(String)
    
    
    
    
    
  