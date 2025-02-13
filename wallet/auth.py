from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .models import User
from . import models
from . import token, database
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError





SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        print(f"Received Token: {token}")  # Debugging step
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Debugging step
        
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise credentials_exception

        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")