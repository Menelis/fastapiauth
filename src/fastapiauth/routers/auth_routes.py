from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncConnection
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import timedelta

from src.fastapiauth.security.bearer import JwtBearer
from src.fastapiauth.database.database import get_database
from src.fastapiauth.schemas.user_schemas import User, UserCreate, UserUpdate, TokenResponse, UserLogin
from src.fastapiauth.security.auth import create_access_token, decode_access_token
from src.fastapiauth import TOKEN_EXPIRE_MINUTES
from src.fastapiauth.repository.user_repository import UserRepository

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

AUTH_HEADER = { "WWW-Authenticate": "Bearer" }

def http_exception(detail: str = "Invalid Token",
                           status_code: int = status.HTTP_401_UNAUTHORIZED) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=AUTH_HEADER
    )

async def get_current_user(token: str = Depends(JwtBearer()),
                           db_session: AsyncConnection = Depends(get_database)):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise http_exception()
    except ExpiredSignatureError:
        raise http_exception(detail="Token is expired")
    except InvalidTokenError:
        raise http_exception()
    
    user = await UserRepository(db_session).get_by_email(username)
    if user is None:
        raise http_exception(detail="User does not exist")
    return user

@auth_router.post("/signin", response_model=TokenResponse, tags=["Token"])
async def sign_in(
    user_login: UserLogin,
    db_session: AsyncConnection = Depends(get_database)):
    
    user = await UserRepository(db_session).authenticate(user_login)
    if not user:
        raise http_exception(detail="Invalid username or password")
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


    