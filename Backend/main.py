from datetime import timedelta
from typing import Annotated
from dotenv import load_dotenv
from os import getenv

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


from functions import auth, db
from datamodels import User, Token, Team, Equipment

load_dotenv(".env")
app = FastAPI()


@app.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
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
@app.get("/org")
def get_curr_org(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    curr_org = db.get_current_org(getenv("DB_URL"))
    return curr_org


@app.get("/org/coaches")
def get_curr_coaches(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    curr_org = db.get_current_coaches(getenv("DB_URL"))
    return curr_org


@app.post("/org/coaches")
def edit_coach(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )


@app.get("/org/players")
def get_curr_players(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    curr_org = db.get_current_players(getenv("DB_URL"))
    return curr_org


@app.post("/org/players")
def edit_player(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )


@app.get("/org/equipment")
def get_curr_equipment(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    curr_org = db.get_current_equipment(getenv("DB_URL"))
    return curr_org


@app.post("/org/equipment")
def edit_equip(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
