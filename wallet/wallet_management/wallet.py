from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import RegisterUser, ShowProfile, TopUp, VerifyAccount, ShowReceiverAccount
from ..database import get_db
from ..repository import users as userRepo
from .. import auth



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
def send_money(request: TopUp, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.send_money(user.id, request, db, user)



@router.post("/verify", status_code=status.HTTP_200_OK, response_model=ShowReceiverAccount)
def verify_account(request: VerifyAccount, user: str = Depends(auth.get_current_user),  db: Session = Depends(get_db)):
    return userRepo.verify_account(user.id, request, db, user)