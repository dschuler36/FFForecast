CREATE TABLE weekly_roster (
    season INT NOT NULL,
    week INT NOT NULL,
    position VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    player_id VARCHAR NOT NULL,
    player_name VARCHAR NOT NULL,
    team VARCHAR NOT NULL,
    PRIMARY KEY (season, week, player_id)
);