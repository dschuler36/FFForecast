CREATE TABLE weekly_stats (
    player_id VARCHAR,
    player_display_name VARCHAR,
    position VARCHAR,
    headshot_url VARCHAR,
    team VARCHAR,
    season INT,
    week INT,
    opponent VARCHAR,
    completions INT,
    attempts INT,
    passing_yards REAL,
    passing_tds INT,
    interceptions REAL,
    fumbles REAL,
    sacks REAL,
    sack_yards REAL,
    passing_air_yards REAL,
    passing_yards_after_catch REAL,
    passing_first_downs REAL,
    passing_epa REAL,
    passing_2pt_conversions INT,
    pacr REAL,
    dakota REAL,
    carries INT,
    rushing_yards REAL,
    rushing_tds INT,
    rushing_first_downs REAL,
    rushing_epa REAL,
    rushing_2pt_conversions INT,
    receptions INT,
    targets INT,
    receiving_yards REAL,
    receiving_tds INT,
    receiving_air_yards REAL,
    receiving_yards_after_catch REAL,
    receiving_first_downs REAL,
    receiving_epa REAL,
    receiving_2pt_conversions INT,
    racr REAL,
    target_share REAL,
    air_yards_share REAL,
    wopr REAL,
    special_teams_tds REAL,
    fantasy_points REAL,
    fantasy_points_ppr REAL,
    UNIQUE (player_id, week, season)
);