from datamodels import User, UserInDB

import sqlite3


def get_user(db: str, username: str, include_pwd: bool = True):
    try:
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

    finally:
        pass
        cur.close()
        con.close()


def get_current_players(db: str, cur):
    con = sqlite3.connect(db)
    cur = con.cursor()
    players = {}
    player_info = cur.execute("SELECT username,teamName FROM player_info pi\
                            JOIN user_auth_info uai ON pi.pID = uai.userID\
                            JOIN team_info ti ON pi.tID = ti.teamID").fetchall()
    for player in player_info:
        if players.get(player[0]):
            players[player[0]]["teams"].add(player[1])
        else:
            players[player[0]] = {"teams": set()}
            players[player[0]]["teams"].add(player[1])
    return players


def get_current_coaches(db: str, cur):
    con = sqlite3.connect(db)
    cur = con.cursor()
    coaches = {}
    coach_info = cur.execute("SELECT username,teamName FROM coach_info ci\
                            JOIN user_auth_info uai ON ci.coachID = uai.userID\
                            JOIN team_info ti ON ci.tID = ti.teamID").fetchall()
    for coach in coach_info:
        if coaches.get(coach[0]):
            coaches[coach[0]]["teams"].add(coach[1])
        else:
            coaches[coach[0]] = {"teams": set()}
            coaches[coach[0]]["teams"].add(coach[1])
    return coaches


def get_current_equipment(db: str, cur):
    equipment = {}
    equip_info = cur.execute("SELECT equipName,unitPrice,initQuantity,currQuantity\
                                FROM equipment_info")
    for equip in equip_info:
        equipment[equip[0]] = {"unitPrice": equip[1], "initQuantity": equip[2],
                               "currQuantity": equip[3]}
    return equipment


def get_current_org(db: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        teams = {}
        coaches = get_current_coaches(db, cur)
        players = get_current_players(db, cur)
        equipment = get_current_equipment(db, cur)
        team_info = cur.execute("SELECT teamName FROM team_info").fetchall()
        coach_counts = cur.execute("SELECT teamName, COUNT(coachID) FROM coach_info ci\
                                   JOIN team_info ti ON ti.teamID = ci.tID\
                                   GROUP BY teamName").fetchall()
        player_counts = cur.execute("SELECT teamName, COUNT(pID) FROM player_info pi\
                                   JOIN team_info ti ON ti.teamID = pi.tID\
                                   GROUP BY teamName").fetchall()
        for team in team_info:
            teams[team[0]] = {"players": 0, "coaches": 0}
        for player in player_counts:
            teams[player[0]]["players"] = player[1]
        for coach in coach_counts:
            teams[coach[0]]["coaches"] = coach[1]

        return {"teams": teams, "coaches": coaches,
                "players": players, "equipment": equipment
                }
    finally:
        cur.close()
        con.close()
