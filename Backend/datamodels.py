from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    id: int
    username: str
    category: str


class Team(BaseModel):
    id: int
    name: str


class Equipment(BaseModel):
    id: int
    name: str
    unit_price: float
    max_quantity: int
    curr_quantity: int


class UserInDB(User):
    hashed_password: str
