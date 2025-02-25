import os
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_jwt_token(data: dict, expires_delta: Optional[int] = None):
    expire = datetime.utcnow() + timedelta(minutes=expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def decode_jwt_token(token: str):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    return payload

def get_current_user(token: str = Depends(oath2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt_token(token)
        username: str = payload.get("email")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return username


def hashed_password(password: str):
    return pwd_context.hash(password)


