from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.schemas.user import UserRegistration
from app.core.security import create_jwt_token, hashed_password, pwd_context
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db.models import Users
from app.kafka.email_producer import send_email_to_kafka

users_router = APIRouter(prefix="/auth", tags=["auth"])


@users_router.post("/register")
async def register(data: UserRegistration, session: Session = Depends(get_db)):
    if data:
        password = hashed_password(data.password)
        try:
            session.add(Users(email=data.email, name=data.name, password=password))
            if send_email_to_kafka(data.email, data.name):
                session.commit()
                return {"added data": data}
            return {"message": "Email not sent"}
        except sqlalchemy.exc.IntegrityError as e:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)



@users_router.post("/login")
async def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    try:
        user = session.query(Users).filter(Users.email == user_login.username).first()
        if user and pwd_context.verify(user_login.password, user.password):
            token = create_jwt_token({"email": user_login.username, "password": user_login.password})
            return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.detail)