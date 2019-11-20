DROP TABLE IF EXISTS participant;

CREATE TABLE participant (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    pct_pings_completed FLOAT(24) NOT NULL,
    amount_earned FLOAT(24) NOT NULL,
    completion_streak INTEGER NOT NULL,
    activity_low_stress TEXT NOT NULL,
    activity_happiness TEXT NOT NULL
);
