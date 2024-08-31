`CREATE TABLE weekly_predictions_dk_dfs (
    player_id VARCHAR(255),
    season INT,
    week INT,
    fantasy_points FLOAT8,
    PRIMARY KEY (season, week, player_id)
);
`