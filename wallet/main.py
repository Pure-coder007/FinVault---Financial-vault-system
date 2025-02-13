from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, login
from .wallet_management import wallet



app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(wallet.router)