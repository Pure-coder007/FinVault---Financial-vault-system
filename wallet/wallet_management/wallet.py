from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ..schemas import RegisterUser, ShowProfile, TopUp, VerifyAccount, ShowReceiverAccount, LockFunds, LockedResponse, TransactionFilter
from ..database import get_db
from ..repository import users as userRepo
from .. import auth
from ..models import User
from typing import Optional



router = APIRouter(
    prefix="/wallet",
    tags=["Wallet Management"],
    responses={404: {"description": "Not found"}},
    )


@router.get("/", status_code=status.HTTP_200_OK)
def get_wallet_balance(user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return userRepo.get_wallet_balance(user.id, db, user)



@router.post("/", status_code=status.HTTP_200_OK)
def top_up_account(request: TopUp, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.add_funds(user.id, request, db, user)


@router.post("/transfer/", status_code=status.HTTP_200_OK)
def send_money(request: TopUp, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    return userRepo.send_money(user.id, request, db, user, background_tasks)



@router.post("/verify", status_code=status.HTTP_200_OK, response_model=ShowReceiverAccount)
def verify_account(request: VerifyAccount, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.verify_account(user.id, request, db, user)



@router.post("/lock", status_code=status.HTTP_200_OK)
def lock_funds(request: LockFunds, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.lock_funds(user.id, request, db, user)



@router.get("/limit", status_code=status.HTTP_200_OK)
def get_wallet_limit(user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.get_wallet_limit(user.id, db, user)


from fastapi import Query

@router.get("/transaction_history", status_code=status.HTTP_200_OK)
def get_transaction_history(
    start_date: str,
    end_date: str,
    transaction_type: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_order: str = "desc",
    user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    request = TransactionFilter(
        start_date=start_date,
        end_date=end_date,
        transaction_type = transaction_type.lower() if transaction_type else None,
        page=page,
        limit=limit,
        sort_order=sort_order
    )

    return userRepo.get_transaction_history(user.id, request, db, user)
