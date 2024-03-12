from datamodels import User, UserInDB

import sqlite3


def get_user(db: str, username: str, include_pwd: bool = True):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        user_data = cur.execute("SELECT * FROM user_info WHERE username = ?", (username,)).fetchone()
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


def get_current_players(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    players = {}
    player_info = cur.execute("SELECT username,teamName FROM player_info pi\
                            JOIN user_info uai ON pi.pID = uai.userID\
                            JOIN team_info ti ON pi.tID = ti.teamID").fetchall()
    for player in player_info:
        if players.get(player[0]):
            players[player[0]]["teams"].add(player[1])
        else:
            players[player[0]] = {"teams": set()}
            players[player[0]]["teams"].add(player[1])
    return players


def get_current_coaches(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    coaches = {}
    coach_info = cur.execute("SELECT username,teamName FROM coach_info ci\
                            JOIN user_info uai ON ci.coachID = uai.userID\
                            JOIN team_info ti ON ci.tID = ti.teamID").fetchall()
    for coach in coach_info:
        if coaches.get(coach[0]):
            coaches[coach[0]]["teams"].add(coach[1])
        else:
            coaches[coach[0]] = {"teams": set()}
            coaches[coach[0]]["teams"].add(coach[1])
    return coaches


def get_current_equipment(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    equipment = {}
    equip_info = cur.execute("SELECT equipName,unitPrice,initQuantity,currQuantity\
                                FROM equipment_info")
    for equip in equip_info:
        equipment[equip[0]] = {"unitPrice": equip[1], "initQuantity": equip[2],
                               "currQuantity": equip[3]}
    return equipment


def get_current_teams(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    teams = {}
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
    return teams


def get_current_org(db: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        teams = get_current_teams(db, cur)
        coaches = get_current_coaches(db, cur)
        players = get_current_players(db, cur)
        equipment = get_current_equipment(db, cur)
        return {"teams": teams, "coaches": coaches,
                "players": players, "equipment": equipment
                }
    finally:
        cur.close()
        con.close()


def insert_equipment(db: str, name: str, unit_price: float, init_quantity: int):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("INSERT OR IGNORE INTO equipment_info\
                    (equipName, unitPrice, initQuantity, currQuantity)\
                    VALUES (?,?,?,?)", (name, unit_price, init_quantity, init_quantity))
        con.commit()
        return "Inserted equipment"
    finally:
        cur.close()
        con.close()


def insert_team(db: str, team: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("INSERT OR IGNORE INTO team_info (teamName) VALUES (?)", (team,))
        con.commit()
        return f"Inserted {team}"
    finally:
        cur.close()
        con.close()


def assign_user(db: str, user: str, team: str, type: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        u_id = cur.execute("SELECT userID FROM user_info WHERE username=?",
                           (user,)).fetchone()[0]
        t_id = cur.execute("SELECT teamID FROM team_info WHERE teamName=?",
                           (team,)).fetchone()[0]
        if type == "coach":
            assigned_check = cur.execute("SELECT COUNT(*) FROM coach_info\
                                        WHERE (coachID=?) AND (tID=?)", (u_id, t_id)).fetchone()[0]
            if assigned_check > 0:
                return f"{user} already assigned to {team} as {type}"
            else:
                cur.execute("INSERT INTO coach_info (coachID,tID) VALUES (?,?)", (u_id, t_id))
                con.commit()
                return f"Assigned {user} to {team} as {type}"
        elif type == "player":
            assigned_check = cur.execute("SELECT COUNT(*) FROM player_info\
                                      WHERE (pID=?) AND (tID=?)", (u_id, t_id)).fetchone()[0]
            if assigned_check > 0:
                return f"{user} already assigned to {team} as {type}"
            else:
                cur.execute("INSERT INTO player_info (pID,tID) VALUES (?,?)", (u_id, t_id))
                con.commit()
                return f"Assigned {user} to {team} as {type}"
    finally:
        cur.close()
        con.close()


def unassign_user(db: str, user: str, team: str, type: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        u_id = cur.execute("SELECT userID FROM user_info WHERE username=?",
                           (user,)).fetchone()[0]
        t_id = cur.execute("SELECT teamID FROM team_info WHERE teamName=?",
                           (team,)).fetchone()[0]
        if type == "coach":
            assigned_check = cur.execute("SELECT COUNT(*) FROM coach_info\
                                        WHERE (coachID=?) AND (tID=?)", (u_id, t_id)).fetchone()[0]
            if assigned_check == 0:
                return f"{user} not assigned to {team} as {type}"
            else:
                cur.execute("DELETE FROM coach_info WHERE coachID = ? AND tID = ?", (u_id, t_id))
                con.commit()
                return f"Removed {user} from {team} as {type}"
        elif type == "player":
            assigned_check = cur.execute("SELECT COUNT(*) FROM player_info\
                                      WHERE (pID=?) AND (tID=?)", (u_id, t_id)).fetchone()[0]
            if assigned_check == 0:
                return f"{user} not assigned to {team} as {type}"
            else:
                cur.execute("DELETE FROM player_info WHERE pID = ? AND tID = ?", (u_id, t_id))
                con.commit()
                return f"Removed {user} from {team} as {type}"
    finally:
        cur.close()
        con.close()


def delete_equip(db: str, equip_name: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("DELETE FROM equipment_info WHERE equipName = ?", (equip_name,))
        con.commit()
        return f"{equip_name} deleted from library"
    finally:
        cur.close()
        con.close()


def delete_user(db: str, user: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("DELETE FROM user_info WHERE username = ?", (user,))
        con.commit()
        return f"{user} deleted from library"
    finally:
        cur.close()
        con.close()


def delete_team(db: str, team: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("DELETE FROM team_info WHERE teamName = ?", (team,))
        con.commit()
        return f"{team} deleted from library"
    finally:
        cur.close()
        con.close()
