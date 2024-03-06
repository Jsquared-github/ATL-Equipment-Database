PRAGMA foreign_keys = ON;

CREATE TABLE user_auth_info(
    userID INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    pass TEXT,
    category TEXT
);

CREATE TABLE team_info(
    teamID INTEGER PRIMARY KEY,
    teamName TEXT
);

CREATE TABLE equipment_info(
    equipmentID INTEGER PRIMARY KEY,
    equipName TEXT,
    unitPrice FLOAT,
    initQuantity INTEGER,
    currQuantity INTEGER
);

CREATE TABLE player_info(
    pID INTEGER,
    tID INTEGER,
    PRIMARY KEY(pID,tID),
    FOREIGN KEY(pID) REFERENCES user_auth_info(userID),
    FOREIGN KEY(tID) REFERENCES team_info(teamID)
)WITHOUT ROWID;

CREATE TABLE coach_info(
    coachID INTEGER,
    tID INTEGER,
    PRIMARY KEY(coachID,tID),
    FOREIGN KEY(coachID) REFERENCES user_auth_info(userID),
    FOREIGN KEY(tID) REFERENCES team_info(teamID)
)WITHOUT ROWID;

CREATE TABLE activity_log(
    cID INTEGER,
    tID INTEGER,
    coDate TEXT,
    eID INTEGER,
    equipDiff INTEGER,
    PRIMARY KEY(cID,tID, coDate),
    FOREIGN KEY(cID) REFERENCES coach_info(coachID),
    FOREIGN KEY(tID) REFERENCES team_info(teamID),
    FOREIGN KEY(eID) REFERENCES equipment_info(equpmentID)
)WITHOUT ROWID;