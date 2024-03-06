from datetime import datetime, timedelta, timezone
from typing import Annotated
from dotenv import load_dotenv
import sqlite3

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from os import getenv

load_dotenv(".env")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    category: str


class UserInDB(User):
    hashed_password: str


def verify_password(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_pwd(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    con = sqlite3.connect(db)
    cur = con.cursor()
    user_data = cur.execute("SELECT * FROM user_auth_info WHERE username = ?", (username,)).fetchone()
    user = {"id": user_data[0], "username": user_data[1],
            "hashed_password": user_data[2], "category": user_data[3]
            }
    return UserInDB(**user)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("SECRET_KEY"), getenv("ALGORITHM"))
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(getenv("DB_URL"), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
async def login_for_access_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(getenv("DB_URL"), form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expirey = timedelta(minutes=int(getenv("DEFAULT_EXPIRE")))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=expirey)
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/users/me/")
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    if current_user.category == "user":
        return {"Access_Level": "user"}
    elif current_user.category == "coach":
        return {"Access_Level": "coach"}
    elif current_user.category == "admin":
        return {"Access_Level": "admin"}
    return current_user
