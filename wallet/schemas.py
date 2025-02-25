from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import asc, desc



class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    phone: str
    transaction_pin: str
    bvn: Optional[str] = None
    nin: Optional[str] = None

    class Config:
        from_attributes = True
        
        
class ShowProfile(BaseModel):
    username: str
    email: str
    phone: str
    bvn: Optional[str]
    nin: Optional[str]
    wallet_balance: float
    book_balance: float
    account_number: str
    level_1: bool
    level_2: bool
    level_3: bool
    created_at: datetime

    class Config:
        from_attributes = True
        
        

class TopUp(BaseModel):
    account_number: str
    amount: float
    transaction_pin: str
    narration: Optional[str] = None
    
    class Config:
        from_attributes = True
    
    
class VerifyAccount(BaseModel):
    account_number: str
    
    class Config:
        from_attributes = True
    

class ShowReceiverAccount(BaseModel):
    username: str
    account_number: str
    phone: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        
        
        
class LockFunds(BaseModel):
    amount: float
    release_date: datetime
    transaction_pin: str
    
    class Config:
        from_attributes = True
        
        

class LockedResponse(BaseModel):
    locked_amount: float
    release_date: datetime
    
    class Config:
        from_attributes = True
        
        



class TransactionFilter(BaseModel):
    start_date: str
    end_date: str
    page: int = 1
    transaction_type: Optional[str] = None 
    limit: int = 10  
    sort_order: str = "desc"  