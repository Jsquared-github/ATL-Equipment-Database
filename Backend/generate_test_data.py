import sqlite3
import random


from functions.password import get_password


users = [
    ("user1", "user1_pass", "user"),
    ("user2", "user2_pass", "user"),
    ("user3", "user3_pass", "user"),
    ("user4", "user4_pass", "user"),
    ("user5", "user5_pass", "user"),
    ("coach1", "coach1_pass", "coach"),
    ("coach2", "coach2_pass", "coach"),
    ("coach3", "coach3_pass", "coach"),
    ("coach4", "coach4_pass", "coach"),
    ("coach5", "coach5_pass", "coach"),
    ("admin", "admin_pass", "admin"),
]

teams = [
    "team1",
    "team2",
    "team3"
]

equipments = [
    ("soccer_ball_small", 1.00, 100, 100),
    ("soccer_ball_medium", 3.00, 100, 100),
    ("soccer_ball_large", 5.00, 100, 100),
    ("circular_cone_thingy", 1.50, 100, 100),
    ("mini_goal", 10.00, 10, 10)
]

max_user_id, max_team_id, max_equip_id = (len(users), len(teams), len(equipments))


conn = sqlite3.connect("database/library.db")
cur = conn.cursor()
cur.execute("DELETE FROM user_auth_info")
cur.execute("DELETE FROM equipment_info")
cur.execute("DELETE FROM team_info")
cur.execute("DELETE FROM player_info")
cur.execute("DELETE FROM coach_info")
conn.commit()
cur.execute("VACUUM")
conn.commit()
for user in users:
    cur.execute("INSERT INTO user_auth_info (username,pass,category) VALUES (?,?,?)",
                (user[0], get_password(user[1]), user[2])
                )
    conn.commit()

for team in teams:
    cur.execute("INSERT INTO team_info (teamName) VALUES (?)",
                (team,)
                )
    conn.commit()

for equipment in equipments:
    cur.execute("INSERT INTO equipment_info (equipName,unitPrice,initQuantity,currQuantity)\
                 VALUES (?,?,?,?)",
                (equipment[0], equipment[1], equipment[2], equipment[3])
                )
    conn.commit()

for idx in range(5):
    rand_team = random.randint(1, max_team_id)
    cur.execute("INSERT INTO player_info (pID,tID) VALUES (?,?)", (idx, rand_team))
    conn.commit()

for idx in range(5, 10):
    rand_team = random.randint(1, max_team_id)
    cur.execute("INSERT INTO coach_info (coachID,tID) VALUES (?,?)", (idx, rand_team))
    conn.commit()

cur.close()
conn.close()
