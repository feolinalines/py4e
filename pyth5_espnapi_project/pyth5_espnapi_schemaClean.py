import sqlite3

connection = sqlite3.connect('teamstatsdb.sqlite')
cursor     = connection.cursor()


# Drop any existing tables and create fresh copies
#
cursor.executescript('''
DROP TABLE IF EXISTS sport;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS season;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS player;

CREATE TABLE sport (
    id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

INSERT INTO sport(name) VALUES ('Football');
INSERT INTO sport(name) VALUES ('Basketball');
INSERT INTO sport(name) VALUES ('Soccer');
INSERT INTO sport(name) VALUES ('Baseball');

CREATE TABLE team (
    id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    display_name         TEXT,
    short_name           TEXT,
    nickname             TEXT,
    abbreviation         TEXT,
    color                TEXT,
    espn_id              INTEGER,
    espn_url_roster      TEXT,
    espn_url_schedule    TEXT,
    espn_url_statistics  TEXT,
    espn_url_team        TEXT,
    espn_url_logo        TEXT,
    sport_id             INTEGER
);

INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Auburn',          2,   (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Arkansas',        8,   (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Arizona State',   9,   (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Arizona',         12,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Cal Poly',        13,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('San Diego State', 21,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('San Jose State',  23,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Stanford',        24,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('California',      25,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('UCLA',            26,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('USC',             30,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Colorado State',  36,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Colorado',        38,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('UConn',           41,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Florida State',   52,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Florida State',   57,  (SELECT id FROM sport WHERE name = 'Football'));


INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Georgia',         61,  (SELECT id FROM sport WHERE name = 'Football'));

INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Notre Dame',      87,  (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Michigan',        130, (SELECT id FROM sport WHERE name = 'Football'));
INSERT INTO team (short_name, espn_id, sport_id) VALUES ('Texas',           251, (SELECT id FROM sport WHERE name = 'Football'));

CREATE TABLE season (
    id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team_id              INTEGER,
    sport_id             INTEGER,
    year                 INTEGER,
    record_summary       TEXT,
    standing_summary     TEXT,
    espn_url_roster      TEXT,
    espn_url_schedule    TEXT,
    espn_url_statistics  TEXT
);

CREATE TABLE event (
    id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    season_id            INTEGER,
    season_type_id       INTEGER,
    season_type_name     TEXT,
    week_number          INTEGER,
    week_name            TEXT,
    date_time            TEXT,
    short_name           TEXT,
    name                 TEXT,
    home_team_id         INTEGER,
    home_team_score      INTEGER,
    away_team_id         INTEGER,
    away_team_score      INTEGER,
    result               TEXT,
    score                TEXT,
    record_overall       TEXT,
    record_conference    TEXT,
    high_passer_id       INTEGER,
    high_passing_yards   INTEGER,
    high_rusher_id       INTEGER,
    high_rushing_yards   INTEGER,
    high_receiver_id     INTEGER,
    high_receiving_yards INTEGER
);

CREATE TABLE player (
    id                   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team_id              INTEGER,
    last_name            TEXT,
    display_name         TEXT

);

''')

connection.commit()
cursor.close()