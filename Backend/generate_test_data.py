import sqlite3
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pwd(password):
    return pwd_context.hash(password)


def insert_user(username: str, password: str, category: str):
    con = sqlite3.connect("database/database.db")
    cur = con.cursor()
    cur.execute("SELECT username FROM user_auth_info WHERE username = ?", (username,))
    if cur.rowcount:
        print(f"Username '{username}' is already in use")
    else:
        pass_hash = get_pwd(password)
        with open("database/sql/updates/insert_user_auth.sql", 'r') as f:
            statement = f.read()
            cur.execute(statement, (username, pass_hash, category))
            con.commit()
    cur.close()
    con.close()


insert_user("test_user", "user_pass", "user")
insert_user("test_coach", "coach_pass", "coach")
insert_user("test_admin", "admin_pass", "admin")
