CREATE TABLE depth_chart_tmp (
    team VARCHAR(5),
    player_name VARCHAR,
    position VARCHAR(5),
    depth INT,
    player_id VARCHAR,
    season INT,
    week INT,
    PRIMARY KEY (player_id, season, week)
);