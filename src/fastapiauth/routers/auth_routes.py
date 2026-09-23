from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncConnection
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import timedelta

from ..security.bearer import JwtBearer
from ..database.database import get_database
from ..schemas.user_schemas import User, UserCreate, UserUpdate, TokenResponse, UserLogin
from ..security.auth import create_access_token, decode_access_token
from .. import TOKEN_EXPIRE_MINUTES
from ..repository.user_repository import UserRepository

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

async def get_current_user(token: str = Depends(JwtBearer()),
                           db_session: AsyncConnection = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = decode_access_token(token);
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise credentials_exception
    
    user = await UserRepository(db_session).get_by_email(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exists",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@auth_router.post("/signin", response_model=TokenResponse, tags=["Token"])
async def sign_in(
    user_login: UserLogin,
    db_session: AsyncConnection = Depends(get_database)):
    
    user = await UserRepository(db_session).authenticate(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalud username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expire_in_minutes = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=expire_in_minutes)
    return {"access_token": access_token, "token_type": "Bearer"}

@auth_router.get("/users/me", response_model=User, tags=["Users"])
async def read_self(current_user: User = Depends(get_current_user)):
    return current_user

@auth_router.post("/signup", response_model=User, tags=["Users"])
async def register_user(user: UserCreate,
                        db_session: AsyncConnection = Depends(get_database)):
    return await UserRepository(db_session).register(user)


    