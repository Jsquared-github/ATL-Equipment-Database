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
        if not user_data:
            return None
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
        coaches[coach[0]] = {"coachName": coach[0], "teams": set()}
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
        equipment[equip[0]] = {"equipName": equip[0], "unitPrice": equip[1], "initQuantity": equip[2],
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
        teams[team[0]] = {"teamName": team[0], "players": 0, "coaches": 0}
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
        return (None, None)
    elif period == "day":
        offset = (datetime.now() - timedelta(days=1)).date().isoformat()
        return offset, 1
    elif period == "week":
        offset = (datetime.now() - timedelta(weeks=1)).date().isoformat()
        return offset, 7
    elif period == "month":
        offset = (datetime.now() - timedelta(days=30)).date().isoformat()
        return offset, 30


def calculate_dashboard_metrics(cur, logs: list, days: int | None):
    equips_lost = {}
    dashboard = {"total_equip_lost": 0,
                 "total_cost": 0,
                 "avg_daily_equip_loss": float(0),
                 "avg_daily_cost": float(0),
                 "top_equips_lost": "No Lost Equipment"
                 }
    if days is None:
        if logs:
            start_date = date.fromisoformat(logs[0][2])
        else:
            start_date = date.fromisoformat('2024-01-01')
        end_date = date.today()
        days = (end_date - start_date).days
        if days == 0:
            days = 1
    for log in logs:
        equip_info = cur.execute("SELECT equipName,unitPrice FROM equipment_info\
                                    WHERE equipmentID = ?", (log[0],)).fetchone()
        if not equips_lost.get(equip_info[0]):
            equips_lost[equip_info[0]] = 0
        dashboard["total_equip_lost"] += -log[1]
        equips_lost[equip_info[0]] += -log[1]
        dashboard["total_cost"] += -(log[1]*equip_info[1])

    dashboard["avg_daily_equip_loss"] = round((dashboard["total_equip_lost"]/days), 2)
    dashboard["avg_daily_cost"] = round((dashboard["total_cost"]/days), 2)
    if equips_lost:
        equips_lost = dict(sorted(equips_lost.items(), key=lambda x: -x[1])[:6])
        dashboard["top_equips_lost"] = equips_lost
    return dashboard


def get_coach_stats(cur, period: str | None, days: int | None, metric: str):
    coach_stats = []
    coaches = cur.execute("SELECT userID, username FROM user_info \
                              WHERE category = ?", ("coach",)).fetchall()
    if period is None:
        for coach in coaches:
            coach_metrics = {
                "name": coach[1],
                "total_equip_lost": 0,
                "total_cost": 0,
                "avg_daily_cost": float(0),
                "avg_daily_loss": float(0)
            }
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                            WHERE cID = ?", (coach[0],)).fetchall()
            if days is None:
                start_date = date.fromisoformat(logs[0][2])
                end_date = date.today()
                days = (end_date - start_date).days
                if days == 0:
                    days = 1
            for log in logs:
                equip_info = cur.execute("SELECT equipName,unitPrice FROM equipment_info\
                                    WHERE equipmentID = ?", (log[0],)).fetchone()
                coach_metrics["total_equip_lost"] += -log[1]
                coach_metrics["total_cost"] += -(log[1]*equip_info[1])
            coach_metrics["avg_daily_loss"] = round((coach_metrics["total_equip_lost"]/days), 2)
            coach_metrics["avg_daily_cost"] = round((coach_metrics["total_cost"]/days), 2)
            coach_stats.append(coach_metrics)
    else:
        for coach in coaches:
            coach_metrics = {
                "name": coach[1],
                "total_equip_lost": 0,
                "total_cost": 0,
                "avg_daily_cost": float(0),
                "avg_daily_loss": float(0)
            }
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                            WHERE cID = ? AND coDate >= ?", (coach[0], period)).fetchall()
            if days is None:
                start_date = date.fromisoformat(logs[0][2])
                end_date = date.today()
                days = (end_date - start_date).days
                if days == 0:
                    days = 1
            for log in logs:
                equip_info = cur.execute("SELECT equipName,unitPrice FROM equipment_info\
                                    WHERE equipmentID = ?", (log[0],)).fetchone()
                coach_metrics["total_equip_lost"] += -log[1]
                coach_metrics["total_cost"] += -(log[1]*equip_info[1])
            coach_metrics["avg_daily_loss"] = round((coach_metrics["total_equip_lost"]/days), 2)
            coach_metrics["avg_daily_cost"] = round((coach_metrics["total_cost"]/days), 2)
            coach_stats.append(coach_metrics)
    if metric == "items":
        coach_stats = sorted(coach_stats, key=lambda x: x["total_equip_lost"])
    elif metric == "cost":
        coach_stats = sorted(coach_stats, key=lambda x: x["total_cost"])
    return coach_stats


def get_team_stats(cur, period: str | None, days: int | None, metric: str):
    team_stats = []
    teams = cur.execute("SELECT teamID,teamName FROM team_info").fetchall()
    if period is None:
        for team in teams:
            team_metrics = {
                "name": team[1],
                "total_equip_lost": 0,
                "total_cost": 0,
                "avg_daily_cost": float(0),
                "avg_daily_loss": float(0)
            }
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                            WHERE tID = ?", (team[0],)).fetchall()
            if days is None:
                start_date = date.fromisoformat(logs[0][2])
                end_date = date.today()
                days = (end_date - start_date).days
                if days == 0:
                    days = 1
            for log in logs:
                equip_info = cur.execute("SELECT equipName,unitPrice FROM equipment_info\
                                    WHERE equipmentID = ?", (log[0],)).fetchone()
                team_metrics["total_equip_lost"] += -log[1]
                team_metrics["total_cost"] += -(log[1]*equip_info[1])
            team_metrics["avg_daily_loss"] = round((team_metrics["total_equip_lost"]/days), 2)
            team_metrics["avg_daily_cost"] = round((team_metrics["total_cost"]/days), 2)
            team_stats.append(team_metrics)
    else:
        for team in teams:
            team_metrics = {
                "name": team[1],
                "total_equip_lost": 0,
                "total_cost": 0,
                "avg_daily_cost": float(0),
                "avg_daily_loss": float(0)
            }
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                            WHERE tID = ? AND coDate >= ?", (team[0], period)).fetchall()
            if days is None:
                start_date = date.fromisoformat(logs[0][2])
                end_date = date.today()
                days = (end_date - start_date).days
                if days == 0:
                    days = 1
            for log in logs:
                equip_info = cur.execute("SELECT equipName,unitPrice FROM equipment_info\
                                    WHERE equipmentID = ?", (log[0],)).fetchone()
                team_metrics["total_equip_lost"] += -log[1]
                team_metrics["total_cost"] += -(log[1]*equip_info[1])
            team_metrics["avg_daily_loss"] = round((team_metrics["total_equip_lost"]/days), 2)
            team_metrics["avg_daily_cost"] = round((team_metrics["total_cost"]/days), 2)
            team_stats.append(team_metrics)
    if metric == "items":
        team_stats = sorted(team_stats, key=lambda x: x["total_equip_lost"])
    elif metric == "cost":
        team_stats = sorted(team_stats, key=lambda x: x["total_cost"])
    return team_stats


def get_dashboard(db: str, coach: str | None = None,
                  team: str | None = None, period: str | None = None):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        (offset, days) = get_period(period)
        c_id = get_coach_id(db, coach)
        t_id = get_team_id(db, team)
        if (c_id and t_id and period):
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                               WHERE (cID = ? AND tID = ? AND coDate >= ?)",
                               (c_id, t_id, offset)).fetchall()
            dashboard = calculate_dashboard_metrics(cur, logs, days)
            return dashboard
        elif not (c_id or t_id or period):
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log").fetchall()
            dashboard = calculate_dashboard_metrics(cur, logs, days)
            return dashboard
        elif not period:
            if not t_id:
                logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                                    WHERE (cID = ?)",
                                   (c_id, )).fetchall()
                dashboard = calculate_dashboard_metrics(cur, logs, days)
                return dashboard
            elif not c_id:
                logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                                    WHERE (tID = ?)",
                                   (t_id,)).fetchall()
                dashboard = calculate_dashboard_metrics(cur, logs, days)
                return dashboard
            else:
                logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                                    WHERE (cID = ? AND tID = ?)",
                                   (c_id, t_id)).fetchall()
                dashboard = calculate_dashboard_metrics(cur, logs, days)
                return dashboard
        elif not c_id:
            if not t_id:
                logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                                    WHERE (coDate >= ?)",
                                   (offset,)).fetchall()
                dashboard = calculate_dashboard_metrics(cur, logs, days)
                return dashboard
            else:
                logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                                    WHERE (tID = ? AND coDate >= ?)",
                                   (t_id, offset)).fetchall()
                dashboard = calculate_dashboard_metrics(cur, logs, days)
                return dashboard
        elif not t_id:
            logs = cur.execute("SELECT eID, equipDiff, coDate FROM activity_log\
                               WHERE (cID = ?  AND coDate >= ?)",
                               (c_id, offset)).fetchall()
            dashboard = calculate_dashboard_metrics(cur, logs, days)
            return dashboard
    finally:
        cur.close()
        con.close()


def get_leaderboard(db: str, metric: str, period: str):
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        (offset, days) = get_period(period)
        leaderboard = {"coach_stats": [], "team_stats": []}
        leaderboard["coach_stats"] = get_coach_stats(cur, offset, days, metric)
        leaderboard["team_stats"] = get_team_stats(cur, offset, days, metric)
        return leaderboard
    finally:
        cur.close()
        con.close()
