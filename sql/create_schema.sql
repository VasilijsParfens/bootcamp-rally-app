-- create database
CREATE DATABASE IF NOT EXISTS bootcamp_rally;
USE DATABASE bootcamp_rally;

-- schemas (simpler names)
CREATE SCHEMA IF NOT EXISTS data;   -- cars, teams, tracks
CREATE SCHEMA IF NOT EXISTS races;  -- race info and results
CREATE SCHEMA IF NOT EXISTS wallet; -- money and budgets

-- TABLES

-- car maker
CREATE TABLE IF NOT EXISTS data.manufacturer (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name STRING NOT NULL UNIQUE,
    country STRING
);

-- racing team
CREATE TABLE IF NOT EXISTS data.team (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_name STRING NOT NULL UNIQUE,
    country STRING
);

-- members in the team (drivers, engineers etc.)
CREATE TABLE IF NOT EXISTS data.member (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_id INTEGER REFERENCES data.team(id),
    full_name STRING NOT NULL,
    role STRING
);

-- rally track
CREATE TABLE IF NOT EXISTS data.track (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name STRING NOT NULL UNIQUE,
    surface STRING,             -- tarmac, gravel, snow
    difficulty FLOAT,           -- 0.0 to 1.0
    elevation_gain INT
);

-- car table with stats
CREATE TABLE IF NOT EXISTS data.car (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_id INTEGER REFERENCES data.team(id),
    manufacturer_id INTEGER REFERENCES data.manufacturer(id),
    model STRING NOT NULL,
    year INT,
    hp FLOAT,                   -- horsepower
    weight FLOAT,               -- in kg
    accel FLOAT,                -- 0-100 in sec
    top_speed FLOAT,            -- km/h
    reliability FLOAT,          -- 0.0 to 1.0
    aero FLOAT,                 -- 0.0 to 1.0
    drivetrain STRING,          -- AWD / RWD / FWD
    tire STRING
);

-- WALLET / BUDGET

-- current balance for every team
CREATE TABLE IF NOT EXISTS wallet.team_balance (
    team_id INTEGER PRIMARY KEY REFERENCES data.team(id),
    balance FLOAT NOT NULL
);

-- history of transactions
CREATE TABLE IF NOT EXISTS wallet.transaction (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    team_id INTEGER REFERENCES data.team(id),
    txn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    txn_type STRING,   -- fee / prize / topup
    amount FLOAT,
    balance_after FLOAT
);

-- RACES

-- race events
CREATE TABLE IF NOT EXISTS races.race (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    track_id INTEGER REFERENCES data.track(id),
    race_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    entry_fee FLOAT,
    prize_pool FLOAT
);

-- result for every car
CREATE TABLE IF NOT EXISTS races.result (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    race_id INTEGER REFERENCES races.race(id),
    car_id INTEGER REFERENCES data.car(id),
    team_id INTEGER REFERENCES data.team(id),
    position INT,
    time_minutes FLOAT,
    reward FLOAT,
    penalty FLOAT
);

-- SAMPLE DATA (simple so we can test app)

-- manufacturers
INSERT INTO data.manufacturer (name, country) VALUES
    ('Subaru', 'Japan'),
    ('Ford', 'USA'),
    ('Hyundai', 'Korea');

-- teams
INSERT INTO data.team (team_name, country) VALUES
    ('Blue Rockets', 'Finland'),
    ('Speed Demons', 'USA'),
    ('Desert Kings', 'UAE');

-- members
INSERT INTO data.member (team_id, full_name, role) VALUES
    (1, 'Mika Virtanen', 'Driver'),
    (1, 'Anna Laine', 'Engineer'),
    (2, 'John Smith', 'Driver'),
    (3, 'Ali Hassan', 'Driver');

-- tracks
INSERT INTO data.track (name, surface, difficulty, elevation_gain) VALUES
    ('Snow Rush', 'snow', 0.8, 500),
    ('Gravel Madness', 'gravel', 0.5, 200),
    ('Tarmac Thunder', 'tarmac', 0.3, 100);

-- cars
INSERT INTO data.car (team_id, manufacturer_id, model, year, hp, weight, accel, top_speed, reliability, aero, drivetrain, tire)
VALUES
    (1, 1, 'Impreza WRX', 2019, 300, 1400, 5.2, 240, 0.85, 0.70, 'AWD', 'Snow'),
    (2, 2, 'Focus RS', 2018, 320, 1450, 5.0, 250, 0.80, 0.68, 'AWD', 'Gravel'),
    (3, 3, 'i20 WRC', 2020, 310, 1380, 4.9, 245, 0.82, 0.72, 'AWD', 'Tarmac');

-- team balances (start with 5000)
INSERT INTO wallet.team_balance (team_id, balance) VALUES
    (1, 5000),
    (2, 5000),
    (3, 5000);
