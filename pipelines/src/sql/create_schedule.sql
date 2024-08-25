CREATE TABLE schedule (
    game_id VARCHAR,
    season INT,
    week INT,
    gameday DATE,
    gametime TIME,
    weekdate VARCHAR,
    home_team VARCHAR,
    away_team VARCHAR,
    PRIMARY KEY (game_id)
);