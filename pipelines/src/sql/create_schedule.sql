CREATE TABLE schedule (
    game_id VARCHAR,
    gameday DATE,
    gametime TIME,
    weekdate VARCHAR,
    week INT,
    home_team VARCHAR,
    away_team VARCHAR,
    PRIMARY KEY (game_id)
);