from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    phone: str
    bvn: Optional[int]
    nin: Optional[int]

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