from datetime import timedelta
from typing import Annotated
from dotenv import load_dotenv
from os import getenv

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from functions import auth
from datamodels import User, Token, Team, Equipment

load_dotenv(".env")
app = FastAPI()


@app.post("/login")
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = auth.authenticate_user(getenv("DB_URL"), form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    expirey = timedelta(minutes=int(getenv("DEFAULT_EXPIRE")))
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=expirey)
    return Token(access_token=access_token, token_type="Bearer")


# Use Annotated[User, Depends(auth.resolve_token)] to get current user
