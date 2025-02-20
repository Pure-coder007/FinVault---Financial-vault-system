from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends, BackgroundTasks
from ..schemas import RegisterUser, ShowProfile, TopUp, VerifyAccount, ShowReceiverAccount, LockFunds, TransactionFilter
from ..hashing import Hash, PinHash
from ..database import get_db
from ..models import User, LockedFunds
import random, bcrypt
from datetime import datetime, timedelta
import os
from ..utils.func import *
from .. import auth, token, models
from sqlalchemy import func
from sqlalchemy import asc, desc




# Load environment variables from .env
load_dotenv()




def create_user(
    request: RegisterUser, 
    db: Session, 
    background_tasks: BackgroundTasks,
):
    # Validate password
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must be at least 8 characters long"
        )
    if not any(char.isdigit() for char in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must contain at least one number"
        )
    if not any(char.isupper() for char in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must contain at least one uppercase letter"
        )
    if not any(char.islower() for char in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must contain at least one lowercase letter"
        )
    if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/" for char in request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Password must contain at least one special character"
        )

    # Check if passwords match
    if request.password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords do not match"
        )
    
    # Validate transaction PIN
    if not request.transaction_pin or len(request.transaction_pin) != 4 or not request.transaction_pin.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Transaction PIN must be 4 digits"
        )
    
    # Validate email
    if "@" not in request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid email address"
        )

    # Check if email, phone, or username already exists
    if email_exists(request.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )
    if phone_number_exists(request.phone, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Phone number already exists"
        )
    if username_exists(request.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )

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
        book_balance=50000,
        transaction_pin=PinHash.bcrypt(request.transaction_pin)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send welcome email in the background
    email_subject = "Welcome to Our Platform – Your Account is Ready!"
    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 600px;
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 5px;
            margin: auto;
        }}
        
        .header {{
            background: #007bff;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 28px;
            font-weight: bold;
            border-radius: 10px 10px 0 0;
        }}
        .logo {{
            text-align: center;
            margin-top: 20px; 
            padding-top:5px;
            
        }}
        .logo img {{
            max-width: 80%; /* Ensures the logo is responsive */
            height: auto;    /* Maintains aspect ratio */
            border-radius: 10px; /* Optional: adds rounded corners */
        }}
        .content {{
            padding: 20px;
            font-size: 16px;
            color: #333;
            margin-top: -20px; /* Adjusted margin for better spacing */
        }}
        .content p {{
            line-height: 1.6;
        }}
        
        .footer {{
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #666;
        }}
        .btn {{
            display: inline-block;
            background: #007bff;
            color: white;
            text-decoration: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 20px;
            transition: background 0.3s;
        }}
        .btn:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>

    <div class="container">
        
        <div class="logo">
            <img src="https://res.cloudinary.com/duyoxldib/image/upload/v1740063400/Screenshot_2025-02-20_at_3.55.44_PM_fxktdp.png" alt="Company Logo"> 
        </div>
            
        <div class="content">
            <p>Dear <strong>{new_user.username}</strong>,</p>
            
            <p>Congratulations! Your account has been successfully created, and we are thrilled to welcome you to our community. At FinVault, we strive to provide you with the best services and support to make your experience seamless and enjoyable.</p>
            
            <p><strong>Your Account Number:</strong> {new_user.account_number}</p>

            <p>With your new account, you can:</p>
            <ul>
                <li>Access a wide range of financial services tailored to your needs.</li>
                <li>Manage your transactions effortlessly through our user-friendly interface.</li>
                <li>Receive personalized support from our dedicated customer service team.</li>
            </ul>

            <p>We encourage you to start exploring our platform today. Take advantage of our resources and tools designed to help you achieve your financial goals.</p>
            
            <p>If you have any questions or need assistance, please do not hesitate to reach out to our support team. We are here to help you every step of the way!</p>

            <p>Thank you for choosing FinVault. We look forward to serving you.</p>

            <p>Best regards,</p>
            <p><strong>FinVault Support Team</strong></p>
        </div>

        <div class="footer">
            &copy; {datetime.utcnow().year} FinVault | All rights reserved.
        </div>
    </div>

</body>
</html>

"""

    
    background_tasks.add_task(send_email, email_subject, [new_user.email], email_body)

    return {"message": "User created successfully. A confirmation email has been sent."}





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

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate transaction PIN
    if not bcrypt.checkpw(request.transaction_pin.encode(), user.transaction_pin.encode()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction pin")

    # Validate account number
    if request.account_number != user.account_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid account number")

    # Validate amount
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter a valid amount.")

    # Wallet limits
    MAX_WALLET_BALANCE = 200000.0
    MAX_SINGLE_TRANSACTION = 20000.0

    # If user is Level 1, enforce per-transaction limit
    if user.level_2.lower() == "false" and user.level_3.lower() == "false":
        if request.amount > MAX_SINGLE_TRANSACTION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Level 1 accounts cannot add more than ₦{MAX_SINGLE_TRANSACTION:,.2f} per transaction. Please enter a lower amount."
            )

    # Check if deposit exceeds wallet limit
    if user.wallet_balance + request.amount > MAX_WALLET_BALANCE:
        excess_amount = (user.wallet_balance + request.amount) - MAX_WALLET_BALANCE
        amount_to_wallet = request.amount - excess_amount

        # Add only up to ₦200,000 to the wallet
        user.wallet_balance = MAX_WALLET_BALANCE
        user.book_balance += excess_amount  # Move excess funds to book balance
        db.commit()
        db.refresh(user)

        return {
            "message": f"₦{amount_to_wallet:,.2f} added to main wallet, ₦{excess_amount:,.2f} moved to book balance due to wallet limit.",
            "wallet_balance": f"₦{user.wallet_balance:,.2f}",
            "book_balance": f"₦{user.book_balance:,.2f}"
        }

    # Add funds normally if within limits
    user.wallet_balance += request.amount
    db.commit()
    db.refresh(user)

    return {
        "message": f"₦{request.amount:,.2f} has been added to your wallet.",
        "wallet_balance": f"₦{user.wallet_balance:,.2f}",
        "book_balance": f"₦{user.book_balance:,.2f}"
    }




# Check if account is upgraded
def is_upgraded(id: str, db: Session, current_user: models.User):
    user_level = db.query(User).filter(User.id == id).first()
    if not level_2 or not level_3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot make a transfer of more than ₦20,000.00 until you upgrade your account")
    





    


# Send money to another user
def send_money(id: str, request: TopUp, db: Session, current_user: User):
    user = db.query(models.User).filter(models.User.id == id).first()
    recipient = db.query(models.User).filter(models.User.account_number == request.account_number).first()
    
    if user.id == recipient.id:
        raise HTTPException(status_code=400, detail="Sorry you cannot do a transfer to yourself.")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not recipient:
        raise HTTPException(status_code=400, detail="Invalid account number")
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Please enter a valid amount.")
    if request.amount > user.wallet_balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    if not bcrypt.checkpw(request.transaction_pin.encode(), user.transaction_pin.encode()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction pin")
    
    # Get transaction limits
    max_per_transaction = user.transaction_limit_per_transaction
    max_per_day = user.transaction_limit_per_day

    # Restrict transfer amount based on account level
    if not (user.level_2.lower() == "true" or user.level_3.lower() == "true") and request.amount > max_per_transaction:
        raise HTTPException(
            status_code=403,
            detail=f"You cannot transfer more than ₦{max_per_transaction:,.2f} in a single transaction until you upgrade your account."
        )

    # Check Daily Transfer Limit
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    total_transferred_today = (
        db.query(func.sum(models.Transfers.amount))
        .filter(
            models.Transfers.sender_id == user.id,
            models.Transfers.date_sent >= today_start,
            models.Transfers.date_sent < today_end
        )
        .scalar() or 0
    )

    if total_transferred_today + request.amount > max_per_day:
        raise HTTPException(
            status_code=400,
            detail=f"Daily transfer limit exceeded. You can only transfer ₦{max_per_day:,.2f} per day until you upgrade your account."
        )

    # Create a transfer record with "pending" status
    transfer = models.Transfers(
        sender_id=user.id,
        receiver_id=recipient.id,
        amount=request.amount,
        date_sent=datetime.utcnow(),
        status="pending"
    )
    db.add(transfer)
    db.commit()
    db.refresh(transfer)

    try:
        user.wallet_balance -= request.amount
        recipient.wallet_balance += request.amount

        transfer.status = "completed"
        db.commit()
        db.refresh(user)
        db.refresh(recipient)
        db.refresh(transfer)

        return {"message": f"Transfer of ₦{request.amount:,.2f} successful to {recipient.username}",
                "wallet_balance": f"₦{user.wallet_balance:,.2f}",
                "book_balance": f"₦{user.book_balance:,.2f}",
                "transaction_ref": transfer.transaction_ref,
                "session_id": transfer.session_id}

    except Exception as e:
        db.rollback()  # Ensure rollback on failure

        # Update transaction status to "failed"
        transfer.status = "failed"
        db.commit()
        db.refresh(transfer)

        raise HTTPException(status_code=500, detail="Transaction failed. Please try again.")
    
    




# Verify Account
def verify_account(id: str, request: VerifyAccount, db: Session, current_user: User):
    user = db.query(User).filter(User.id == id).first()
    user_account = db.query(User).filter(User.account_number == request.account_number).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_account:
        raise HTTPException(status_code=400, detail="Invalid account number")
    
    return ShowReceiverAccount(**{**user_account.__dict__})
    




# Locking funds for savings
def lock_funds(id: str, request: LockFunds, db: Session, current_user: User):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Please enter a valid amount.")
    if request.amount > user.wallet_balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    if request.release_date < datetime.now():
        raise HTTPException(status_code=400, detail="Please enter a valid release date.")
    
    if not bcrypt.checkpw(request.transaction_pin.encode(), user.transaction_pin.encode()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction pin")
    
    # Deduct from wallet balance
    user.wallet_balance -= request.amount

    locked_fund = LockedFunds(
        user_id=user.id,
        amount=request.amount,
        release_date=request.release_date.strftime("%Y-%m-%d")
    )
    
    db.add(locked_fund)
    

    db.commit()
    db.refresh(user)

    return {
        "message": f"₦{request.amount:,.2f} has been locked for savings.",
        "wallet_balance": f"₦{user.wallet_balance:,.2f}",
        "book_balance": f"₦{user.book_balance:,.2f}",
        "locked_amount": f"₦{request.amount:,.2f}",  
        "release_date": format_date(request.release_date) 
    }

    



def get_wallet_limit(id: str, db: Session, current_user: User):
    user = db.query(User).filter(User.id == id).first()
    
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.level_1.lower() == "true":
        return {
            "message": f"You are a level one user. Your transaction limit per day is ₦{user.transaction_limit_per_day:,.2f}"
        }
    
    if user.level_2.lower() == "true":
        return {
            "message": f"You are a level two user. Your transaction limit per day is ₦{user.transaction_limit_per_day:,.2f}"
        }
    
    if user.level_3.lower() == "true":
        return {
            "message": f"You are a level three user. Your transaction limit per day is ₦{user.transaction_limit_per_day:,.2f}"
        }
    
    
    return {
        "wallet_limit": f"₦{user.transaction_limit_per_day:,.2f}"
    }
    
    
    





def get_transaction_history(id: str, request: TransactionFilter, db: Session, current_user: models.User):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not request.transaction_type:
        raise HTTPException(status_code=400, detail="Transaction type is required")
    
    
    if request.transaction_type != "credit" and request.transaction_type != "debit":
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Convert date strings to datetime objects safely
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Query transactions where the user is sender or receiver
    transactions_query = db.query(models.Transfers).filter(
        (models.Transfers.sender_id == user.id) | (models.Transfers.receiver_id == user.id),
        models.Transfers.date_sent.between(start_date, end_date)
    )

    # Filter by transaction type if provided
    if request.transaction_type:
        transactions_query = transactions_query.filter(models.Transfers.transaction_type == request.transaction_type)

    # Apply sorting (default: newest first)
    if request.sort_order.lower() == "asc":
        transactions_query = transactions_query.order_by(asc(models.Transfers.date_sent))
    else:
        transactions_query = transactions_query.order_by(desc(models.Transfers.date_sent))
        
    

    # Count total transactions for pagination
    total_count = transactions_query.count()
    total_pages = (total_count + request.limit - 1) // request.limit

    # Apply pagination
    transactions = transactions_query.offset((request.page - 1) * request.limit).limit(request.limit).all()

    return {
        "total_count": total_count,
        "total_pages": total_pages,
        "current_page": request.page,
        "transactions": [
        {
            **transaction.__dict__,
            "amount": f"{transaction.amount:,.2f}",
            "transaction_type": "debit" if transaction.sender_id == user.id else "credit",
            "receiver_name": "Own Wallet" if transaction.receiver.id == user.id else transaction.receiver.username
        }
        for transaction in transactions
    ]
    }