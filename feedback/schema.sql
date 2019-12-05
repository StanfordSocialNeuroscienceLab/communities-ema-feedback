DROP TABLE IF EXISTS participant;

CREATE TABLE participant (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    pct_pings_completed FLOAT(24) NOT NULL,
    amount_earned FLOAT(24) NOT NULL,
    completion_streak INTEGER NOT NULL,
    activity_low_stress TEXT,
    activity_happiness TEXT,
    common_activity_1 TEXT,
    common_activity_2 TEXT,
    common_activity_3 TEXT,
    interaction_partner_1 TEXT,
    interaction_partner_2 TEXT,
    interaction_partner_3 TEXT
);
