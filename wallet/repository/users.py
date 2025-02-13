from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from ..schemas import RegisterUser, ShowProfile, TopUp
from ..hashing import Hash
from ..database import get_db
from ..models import User
import random
from datetime import datetime
from ..utils.func import *
from .. import auth, token, models





# Create a new user
def create_user(request: RegisterUser, db: Session = Depends(get_db)):
    # Validate password
    validate_password(request.password)

    # Check if passwords match
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    

    # Create user instance
    new_user = User(
        username=request.username,
        email=request.email,
        phone=request.phone,
        password=Hash.bcrypt(request.password),
        bvn=request.bvn,
        nin=request.nin,
        account_number=generate_account_number(db),
        wallet_balance=50000,
        book_balance=50000
    )
    
    # check if email is valid
    if "@" not in request.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email address")
    
    if email_exists(request.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    if validate_phone_number(request):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number")
    
    if phone_number_exists(request.phone, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already exists")
    
    if username_exists(request.username, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user





# View own profile
def view_profile(id: str, db: Session, current_user: models.User):
    user = db.query(User).filter(User.id == id).first()
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this profile")

    return ShowProfile(**{**user.__dict__, "bvn": str(user.bvn), "nin": str(user.nin)})

    
    
    


# Get wallet balance
def get_wallet_balance(id: str, db: Session, current_user: models.User):
    user = db.query(User).filter(User.id == id).first()
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this profile")

    return {
    "message": (
        f"Wallet balance as at {datetime.now():%Y-%m-%d %I:%M %p}: ₦{user.wallet_balance:,.2f}, "
        
        f"Book balance as at {datetime.now():%Y-%m-%d %I:%M %p}: ₦{user.book_balance:,.2f}"
    )
}
    
    


# Add funds to wallet
def add_funds(id: str, request: TopUp, db: Session, current_user: models.User):
    user = db.query(User).filter(User.id == id).first()
    print(user.account_number, "user")
    
    if request.account_number != user.account_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account number")
    
    if request.amount <= 0:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter a valid amount.")
    
    if request.amount >= 200000 or user.wallet_balance >= 200000:
        user.book_balance += request.amount
        db.commit()
        db.refresh(user)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account balance cannot exceed ₦200,000.00, but ₦{request.amount:,.2f} has been added to your book balance pending upgrade.")


    # Add funds to wallet
    user.wallet_balance += request.amount
    user.book_balance += request.amount
    db.commit()
    db.refresh(user)

    return {"message": f"₦{request.amount:,.2f} has been added to your wallet.", "wallet_balance": f"₦{user.wallet_balance:,.2f}", "book_balance": f"₦{user.book_balance:,.2f}"}



# Check if account is upgraded
def is_upgraded(id: str, db: Session, current_user: models.User):
    user_level = db.query(User).filter(User.id == id).first()
    if not level_2 or not level_3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot make a transfer of more than ₦20,000.00 until you upgrade your account")
    



# Send money to another user
def send_money(id: str, request: TopUp, db: Session, current_user: User):
    user = db.query(User).filter(User.id == id).first()
    recipient = db.query(User).filter(User.account_number == request.account_number).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not recipient:
        raise HTTPException(status_code=400, detail="Invalid account number")
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Please enter a valid amount.")
    if request.amount > user.wallet_balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Restrict transfer amount based on account level
    if not (user.level_2.lower() == "true" or user.level_3.lower() == "true") and request.amount > 20000:
        print(user.level_2, user.level_3)
        raise HTTPException(
            status_code=403,
            detail="You cannot transfer more than ₦20,000 in a single transfer, until you upgrade your account."
        )

    # Deduct from sender, add to recipient
    user.wallet_balance -= request.amount
    # user.book_balance == user.wallet_balance
    recipient.wallet_balance += request.amount
    db.commit()

    return {"message": f"Transfer of ₦{request.amount:,.2f} successful to {recipient.username}"}
