from datetime import date as dt_date
from typing import Annotated, Optional
from dotenv import load_dotenv
from os import getenv

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from functions import auth, db, password, generate_test_data
from datamodels import User, Token

load_dotenv(".env")
app = FastAPI()
origins = ["https://127.0.0.1:8000", "http://localhost:5173"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/test")
def generate_random_data():
    generate_test_data()
    return "Random Data Generated"


@app.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = auth.authenticate_user(getenv("DB_URL"), form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="Bearer")


@app.get("/dashboard")
def get_dashboard(user: Annotated[User, Depends(auth.resolve_token)], coach: Optional[str] = None,
                  team: Optional[str] = None, period: Optional[str] = None):
    resp = db.get_dashboard(getenv("DB_URL"), coach, team, period)
    return resp


@app.get("/leaderboard")
def get_leaderboard(user: Annotated[User, Depends(auth.resolve_token)], metric: Optional[str] = None,
                    period: Optional[str] = None):
    if metric is None:
        metric = "items_lost"
    resp = db.get_leaderboard(getenv("DB_URL"), metric, period)
    return resp


@app.post("/create-account")
def create_account(username: str, pwd: str, category: str):
    exists = db.check_for_user(getenv("DB_URL"), username)
    if not exists:
        pwd = password.get_password(pwd)
        resp = db.create_user(getenv("DB_URL"), username, pwd, category)
        return resp
    return f"Account with username: {username} already exists. Please choose a different one"


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
    coaches = db.get_current_coaches(getenv("DB_URL"))
    return coaches


@app.delete("/org/coaches/{coach}")
def delete_coach(user: Annotated[User, Depends(auth.resolve_token)], coach: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.delete_user(getenv("DB_URL"), coach)
    return resp


@app.post("/org/coaches/{coach}")
def assign_coach(user: Annotated[User, Depends(auth.resolve_token)], coach: str, team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.assign_user(getenv("DB_URL"), coach, team, "coach")
    return resp


@app.delete("/org/coaches/{coach}/{team}")
def unassign_coach(user: Annotated[User, Depends(auth.resolve_token)], coach: str, team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.unassign_user(getenv("DB_URL"), coach, team, "coach")
    return resp


@app.get("/org/players")
def get_curr_players(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    players = db.get_current_players(getenv("DB_URL"))
    return players


@app.delete("/org/players/{player}")
def delete_player(user: Annotated[User, Depends(auth.resolve_token)], player: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.delete_user(getenv("DB_URL"), player)
    return resp


@app.post("/org/players/{player}")
def assign_player(user: Annotated[User, Depends(auth.resolve_token)], player: str, team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.assign_user(getenv("DB_URL"), player, team, "player")
    return resp


@app.delete("/org/players/{player}/{team}")
def unassign_player(user: Annotated[User, Depends(auth.resolve_token)], player: str, team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.unassign_user(getenv("DB_URL"), player, team, "player")
    return resp


@app.get("/org/teams")
def get_curr_teams(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    teams = db.get_current_teams(getenv("DB_URL"))
    return teams


@app.post("/org/teams/{team}")
def create_team(user: Annotated[User, Depends(auth.resolve_token)], team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.insert_team(getenv("DB_URL"), team)
    return resp


@app.delete("/org/teams/{team}")
def delete_team(user: Annotated[User, Depends(auth.resolve_token)], team: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.delete_team(getenv("DB_URL"), team)
    return resp


@app.get("/org/equipment")
def get_curr_equipment(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    equipment = db.get_current_equipment(getenv("DB_URL"))
    return equipment


@app.post("/org/equipment/{equip}")
def create_equip(user: Annotated[User, Depends(auth.resolve_token)], equip: str,
                 unit_price: float, quantity: int):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.insert_equipment(getenv("DB_URL"), equip, unit_price, quantity)
    return resp


@app.delete("/org/equipment/{equip}")
def delete_equipment(user: Annotated[User, Depends(auth.resolve_token)], equip: str):
    if user.category != "admin":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.delete_equip(getenv("DB_URL"), equip)
    return resp


@app.get("/library")
def get_equipment(user: Annotated[User, Depends(auth.resolve_token)]):
    if user.category == "player":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    resp = db.get_current_equipment(getenv("DB_URL"))
    return resp


@app.post("/library/{equipment}")
def check_out(user: Annotated[User, Depends(auth.resolve_token)],
              coach: str, team: str, equipment: str, quantity: int):
    if user.category == "player":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    db_url = getenv("DB_URL")
    resp = db.checkout_equip(db_url, coach, team, equipment, quantity)
    return resp


@ app.put("/library/{equipment}")
def check_in(user: Annotated[User, Depends(auth.resolve_token)],
             coach: str, team: str, equipment: str, quantity: int):
    if user.category == "player":
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource",
            headers={"Content-Type": "application/json"}
        )
    db_url = getenv("DB_URL")
    date = dt_date.today().isoformat()
    resp = db.return_equip(db_url, coach, team, equipment, quantity)
    return resp
