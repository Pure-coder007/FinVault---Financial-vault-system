from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from ..schemas import RegisterUser, ShowProfile
from ..database import get_db
from ..repository import users as userRepo
from .. import auth

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: RegisterUser, db: Session = Depends(get_db), background_tasks: BackgroundTasks = BackgroundTasks()):
    return userRepo.create_user(user, db, background_tasks)

@router.get("/", status_code=status.HTTP_200_OK, response_model=ShowProfile)
def show_profile(user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return userRepo.view_profile(user.id, db, user)


