import sqlite3
import random


from .password import get_password


def generate_test_data():
    users = [
        ("player1", "player1_pass", "player"),
        ("player2", "player2_pass", "player"),
        ("player3", "player3_pass", "player"),
        ("player4", "player4_pass", "player"),
        ("player5", "player5_pass", "player"),
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

    max_team_id = len(teams)

    try:
        conn = sqlite3.connect("database/library.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM user_info")
        cur.execute("DELETE FROM equipment_info")
        cur.execute("DELETE FROM team_info")
        cur.execute("DELETE FROM player_info")
        cur.execute("DELETE FROM coach_info")
        cur.execute("DELETE FROM activity_log")
        conn.commit()
        cur.execute("VACUUM")
        conn.commit()
        for user in users:
            cur.execute("INSERT INTO user_info (username,pass,category) VALUES (?,?,?)",
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

        for idx in range(1, 6):
            rand_team = random.randint(1, max_team_id)
            cur.execute("INSERT INTO player_info (pID,tID) VALUES (?,?)", (idx, rand_team))
            conn.commit()

        for idx in range(6, 11):
            rand_team = random.randint(1, max_team_id)
            cur.execute("INSERT INTO coach_info (coachID,tID) VALUES (?,?)", (idx, rand_team))
            conn.commit()
    finally:
        cur.close()
        conn.close()
