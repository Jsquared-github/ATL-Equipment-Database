from datamodels import User, UserInDB

import sqlite3


def get_user(db, username: str, include_pwd: bool = True):
    con = sqlite3.connect(db)
    cur = con.cursor()
    user_data = cur.execute("SELECT * FROM user_auth_info WHERE username = ?", (username,)).fetchone()
    if include_pwd:
        user = {"id": user_data[0], "username": user_data[1],
                "hashed_password": user_data[2], "category": user_data[3]
                }
        return UserInDB(**user)
    else:
        user = {"id": user_data[0], "username": user_data[1], "category": user_data[3]}
        return User(**user)
