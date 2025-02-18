from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from .. schemas import RegisterUser
from .. hashing import Hash
from .. database import get_db
from .. models import User
import random
from datetime import datetime


# validate password
# Add funds to a user's wallet
def add_funds(user_id: str, amount: float, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    user.wallet_balance += amount
    db.commit()
    db.refresh(user)
    return user


# Generate a unique 10-digit account number
def generate_account_number(db: Session):
    while True:
        account_number = str(random.randint(1000000000, 9999999999))
        existing_user = db.query(User).filter(User.account_number == account_number).first()
        if not existing_user:
            return account_number
        


def email_exists(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()



def validate_phone_number(request: RegisterUser):
    if len(request.phone) != 13 or not request.phone.isdigit() or not request.phone.startswith("234"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. It must be 13 digits in total and also start with '234'."
        )

    
    
    
def phone_number_exists(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()


def username_exists(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


    



# Validate password
def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one number")
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one lowercase letter")
    if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/" for char in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one special character")
    return password




def format_date(dt):
    day = dt.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return dt.strftime(f"%-d{suffix} %b %Y")





def check_daily_transfer_limit(id: str, db: Session, current_user: User):
    # Fetch the user
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get today's date range
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    # Calculate total transactions for today
    total_transferred_today = (
        db.query(func.sum(models.TransactionHistory.amount))
        .filter(
            models.TransactionHistory.sender == user.id,
            models.TransactionHistory.date >= today_start,
            models.TransactionHistory.date < today_end
        )
        .scalar() or 0  # Default to 0 if there are no transactions
    )

    # Check if total transfers exceed the limit
    if total_transferred_today >= user.transaction_limit_per_day:
        raise HTTPException(status_code=400, detail="Daily transfer limit exceeded.")

    return {
        "message": "You have not exceeded your daily transfer limit.",
        "total_transferred_today": f"₦{total_transferred_today:,.2f}",
        "daily_limit": f"₦{user.transaction_limit_per_day:,.2f}"
    }