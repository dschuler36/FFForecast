CREATE TABLE job_tracker (
    job_id SERIAL PRIMARY KEY,
    job VARCHAR(255) NOT NULL,
    status VARCHAR,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    stats_season INTEGER,
    stats_week INTEGER,
    roster_season INTEGER,
    roster_week INTEGER,
    depth_season INTEGER,
    depth_week INTEGER,
    completed_time TIMESTAMP
);
