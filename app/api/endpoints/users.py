from typing import Annotated
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from app.api.schemas.user import UserRegistration
from app.core.security import create_jwt_token, hashed_password, pwd_context
from app.db.database import get_db
from app.db.models import Users
from app.kafka.email_producer import send_email_to_kafka

users_router = APIRouter(prefix="/auth", tags=["auth"])


@users_router.post("/register")
async def register(data: UserRegistration, session: AsyncSession = Depends(get_db)):
    if data:
        password = hashed_password(data.password)
        try:
            obj = Users(email=data.email, name=data.name, password=password)
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                try:
                    await send_email_to_kafka(data.email, data.name)
                except Exception as e:
                    return {"message": f"❌ User {data.name} hasn't been added, because there is a problem with kafka. Error: {e}"}
                return {"added data": data}
            except TypeError as e:
                return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                     detail=f'Trying to insert duplicated value. Error: {e}')
        except sqlalchemy.exc.IntegrityError as e:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)


@users_router.post("/login")
async def login(user_login: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_db)):
    try:
        result = await session.execute(select(Users).filter(Users.email == user_login.username))
        user = result.scalars().first()
        if user and pwd_context.verify(user_login.password, user.password):
            token = create_jwt_token({"email": user_login.username, "password": user_login.password})
            return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)
