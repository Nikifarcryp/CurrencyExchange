from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import UserRegistration
from app.core.security import create_jwt_token, hashed_password, pwd_context
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import Users

users_router = APIRouter(prefix="/auth", tags=["auth"])


@users_router.post("/register")
async def register(data: UserRegistration, session: Session = Depends(get_db)):
    if data:
        password = hashed_password(data.password)
        session.add(Users(email=data.email, name=data.name, password=password))
        session.commit()
        return {"added data": data}


@users_router.post("/login")
async def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    try:
        user = session.query(Users).filter(Users.email == user_login.username).first()
        if user and pwd_context.verify(user_login.password, user.password):
            token = create_jwt_token({"email": user_login.username, "password": user_login.password})
            return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.detail)