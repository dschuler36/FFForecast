CREATE TABLE accuracy_metrics (
    season INTEGER,
    week INTEGER,
    "MAE" DOUBLE PRECISION,
    "MSE" DOUBLE PRECISION,
    "RMSE" DOUBLE PRECISION,
    "R_squared" DOUBLE PRECISION,
    PRIMARY KEY (season, week)
);