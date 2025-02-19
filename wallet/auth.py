from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .models import User
from . import models
from . import token, database
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the variables
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")






oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])        
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise credentials_exception

        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")