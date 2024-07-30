from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from models import *
from schemas import *
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from settings import *
from logging import getLogger
from main import *
import datetime
from datetime import timedelta
from fastapi import Depends, HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
logger = getLogger(__name__)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def jwt_encode(data: dict):
    return jwt.encode(
        {
            **data,
            "exp": datetime.datetime.utcnow()
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def jwt_decode(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not decode token"
        )


async def auth_account(request: Request = Annotated[Request, Depends(oauth2_scheme)]):
    """Handles authentication"""
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    try:
        payload  = jwt_decode(token)
    except Exception:
        logger.exception("auth_account(jwt_decode): Detokenization failed")
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials(token expired)",
        )
    try:
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="(username None)Invalid authentication credentials",
        )
    except JWTError:
        raise HTTPException(
            headers={"WWW-Authenticate": "Bearer"},
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="(JWT ERROR)Invalid authentication credentials",
        )
