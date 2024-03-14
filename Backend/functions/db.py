from datamodels import User, UserInDB
from datetime import date, timedelta, datetime

import sqlite3


def check_for_user(db: str, username: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        exists = cur.execute("SELECT COUNT(*) FROM user_info\
                    WHERE username = ?", (username,)).fetchone()[0]
        if exists:
            return 1
        return 0
    finally:
        cur.close()
        con.close()


def create_user(db: str, username: str, pwd: str, category: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("INSERT INTO user_info (username,pass, category)\
                    VALUES (?,?,?)", (username, pwd, category))
        con.commit()
        return f"{category} account created"
    finally:
        cur.close()
        con.close()


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
        cur.close()
        con.close()


def get_current_players(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    players = {}
    all_players = cur.execute("SELECT username FROM user_info\
                               WHERE category = 'player'").fetchall()
    player_teams = cur.execute("SELECT username,teamName FROM player_info pi\
                            JOIN user_info ui ON pi.pID = ui.userID\
                            JOIN team_info ti ON pi.tID = ti.teamID").fetchall()
    for player in all_players:
        players[player[0]] = {"teams": set()}
    for player in player_teams:
        players[player[0]]["teams"].add(player[1])
    return players


def get_current_coaches(db: str, cur=None):
    if not cur:
        con = sqlite3.connect(db)
        cur = con.cursor()
    coaches = {}
    all_coaches = cur.execute("SELECT username FROM user_info WHERE category = 'coach'").fetchall()
    coach_teams = cur.execute("SELECT username,teamName FROM coach_info ci\
                            JOIN user_info ui ON ci.coachID = ui.userID\
                            JOIN team_info ti ON ci.tID = ti.teamID").fetchall()
    for coach in all_coaches:
        coaches[coach[0]] = {"teams": set()}
    for coach in coach_teams:
        coaches[coach[0]]["teams"].add(coach[1])
    return coaches


def get_coach_id(db: str, coach: str | None):
    if coach == None:
        return None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        id = cur.execute("SELECT userID FROM user_info \
                    WHERE username = ?", (coach,)).fetchone()[0]
        return id
    finally:
        cur.close()
        con.close()


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


def get_equip_id(db: str, equipment: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        id = cur.execute("SELECT equipmentID FROM equipment_info \
                    WHERE equipName = ?", (equipment,)).fetchone()[0]
        return id
    finally:
        cur.close()
        con.close()


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


def get_team_id(db: str, team: str | None):
    if team == None:
        return None
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        id = cur.execute("SELECT teamID FROM team_info \
                    WHERE teamName = ?", (team,)).fetchone()[0]
        return id
    finally:
        cur.close()
        con.close()


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


def checkout_equip(db: str, coach: int, team: int, equip: int,
                   co_quantity: int):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        co_date = date.today().isoformat()
        c_id = get_coach_id(db, coach)
        t_id = get_team_id(db, team)
        e_id = get_equip_id(db, equip)
        curr_quantity = cur.execute("SELECT currQuantity FROM equipment_info\
                                    WHERE equipName = ?", (equip,)).fetchone()[0]
        entry_exists = cur.execute("SELECT COUNT(*) FROM activity_log\
                                   WHERE (cID = ? AND tID = ? AND eID = ? AND coDate = ?)",
                                   (c_id, t_id, e_id, co_date)).fetchone()[0]
        if curr_quantity < co_quantity:
            return f"There are only {curr_quantity} of {equip} able to be checked out"
        if not entry_exists:
            cur.execute("INSERT INTO activity_log (cID,tID,eID,coDate,equipDiff)\
                        VALUES (?,?,?,?,?)", (c_id, t_id, e_id, co_date, -co_quantity))
            cur.execute("UPDATE equipment_info SET currQuantity = (currQuantity - ?)\
                    WHERE equipmentID = ?", (co_quantity, e_id))
        else:
            cur.execute("UPDATE activity_log SET equipDiff = equipDiff - ?\
                         WHERE (cID = ? AND tID = ? AND eID = ? AND coDate = ?)",
                        (co_quantity, c_id, t_id, e_id, co_date))
            cur.execute("UPDATE equipment_info SET currQuantity = (currQuantity - ?)\
                    WHERE equipmentID = ?", (co_quantity, e_id))
        con.commit()
        return f"Checked out {co_quantity} of {equip}"
    finally:
        cur.close()
        con.close()


def return_equip(db: str, coach: int, team: int, equip: int, ci_quantity: int):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        ci_date = date.today().isoformat()
        c_id = get_coach_id(db, coach)
        t_id = get_team_id(db, team)
        e_id = get_equip_id(db, equip)
        entry_exists = cur.execute("SELECT equipDiff FROM activity_log\
                                   WHERE (cID = ? AND tID = ? AND eID = ? AND coDate = ?)",
                                   (c_id, t_id, e_id, ci_date)).fetchone()
        if not entry_exists:
            return f"{coach} has not checked out {equip} for {team} today"
        elif entry_exists[0] == 0:
            return f"{coach} has returned all checked out {equip} today"
        else:
            cur.execute("UPDATE activity_log SET equipDiff = equipDiff + ?\
                            WHERE (cID = ? AND tID = ? AND eID = ? AND coDate = ?)",
                        (ci_quantity, c_id, t_id, e_id, ci_date))
            cur.execute("UPDATE equipment_info SET currQuantity = currQuantity + ?\
                        WHERE equipmentID = ?", (ci_quantity, e_id))
        con.commit()
        return f"Checked in {ci_quantity} of {equip}"
    finally:
        cur.close()
        con.close()


def get_period(period: str | None):
    if not period:
        return None
    elif period == "day":
        return (datetime.now() - timedelta(days=1)).date()
    elif period == "week":
        return (datetime.now() - timedelta(weeks=1)).date()
    elif period == "month":
        return (datetime.now() - timedelta(days=30)).date()


def dashboard(db: str, coach: str | None = None,
              team: str | None = None, period: str | None = None):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        period = get_period(period)
        c_id = get_coach_id(db, coach)
        t_id = get_team_id(db, team)
        if (c_id and t_id and period):
            # all filters
            pass
        elif not (c_id or t_id or period):
            # no filters
            pass
        elif not period:
            if not t_id:
                # coach filter
                pass
            elif not c_id:
                # team filter
                pass
            else:
                # team, coach
                pass
        elif not c_id:
            if not t_id:
                # period filter
                pass
            else:
                pass
                # period, team filter
        else:
            pass
            # period, coach filter
    finally:
        cur.close()
        con.close()
