import numpy as np

from jobs.shared.constants import accuracy_cols
from jobs.shared.logging_config import logger
import pandas as pd
import polars as pl

from jobs.shared.settings import settings


def read_weekly_predictions(season: int, week: int) -> pl.DataFrame:
    df = pd.read_sql(
        sql=f'select * from weekly_predictions_base where season = {season} and week = {week}',
        con=settings.POSTGRES_CONN_STRING
    )
    return pl.from_pandas(df)


def read_half_ppr_predictions(season: int, week: int) -> pl.DataFrame:
    df = pd.read_sql(
        sql=f'select * from weekly_predictions_std_half_ppr where season = {season} and week = {week}',
        con=settings.POSTGRES_CONN_STRING
    )
    return pl.from_pandas(df)


def read_weekly_actuals(season: int, week: int) -> pl.DataFrame:
    df = pd.read_sql(
        sql=f'select * from weekly_stats where season = {season} and week = {week}',
        con=settings.POSTGRES_CONN_STRING
    )
    return pl.from_pandas(df)


def merge_preds_actuals(preds_df: pl.DataFrame, actuals_df: pl.DataFrame) -> pl.DataFrame:

    preds_df = preds_df.select(accuracy_cols)
    actuals_df = actuals_df.select(accuracy_cols)
    return preds_df.join(actuals_df, on=['player_id', 'season', 'week'], suffix='_actual')


def get_fantasy_points_with_actuals(preds_df: pl.DataFrame, fanasy_pts_df: pl.DataFrame) -> pl.DataFrame:
    return preds_df.join(fanasy_pts_df, on=['player_id', 'season', 'week'])


def calculate_differences(merged_df: pl.DataFrame) -> pl.DataFrame:
    for col in accuracy_cols:
        if col not in ['player_id', 'season', 'week']:
            merged_df = merged_df.with_columns((pl.col(f'{col}_actual') - pl.col(col)).alias(f'{col}_diff'))
    return merged_df


def calculate_accuracy_metrics(df: pl.DataFrame, season: int, week: int) -> pl.DataFrame:
    # Ensure the required columns exist
    required_columns = ['fantasy_points', 'fantasy_points_actual', 'fantasy_points_diff']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(
            "DataFrame must contain 'fantasy_points', 'fantasy_points_actual', and 'fantasy_points_diff' columns")

    # Calculate metrics
    mae = df['fantasy_points_diff'].abs().mean()
    mse = (df['fantasy_points_diff'] ** 2).mean()
    rmse = np.sqrt(mse)

    # Calculate R-squared
    y_mean = df['fantasy_points_actual'].mean()
    ss_tot = ((df['fantasy_points_actual'] - y_mean) ** 2).sum()
    ss_res = (df['fantasy_points_diff'] ** 2).sum()
    r_squared = 1 - (ss_res / ss_tot)

    # Create a Polars DataFrame with the metrics
    metrics_df = pl.DataFrame({
        'season': season,
        'week': week,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R_squared': r_squared
    })

    return metrics_df


def write_predictions_diffs(df: pl.DataFrame):
    df.write_database(
        table_name='prediction_diffs',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='append'
    )


def write_accuracy_metrics(df: pl.DataFrame):
    df.write_database(
        table_name='accuracy_metrics',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='append'
    )


def main(season: int, week: int):
    logger.info(f'Running weekly accuracy calculation for season {season} and week {week}')

    # Pull predictions for season / week
    pred_df = read_weekly_predictions(season, week)
    fantasy_points_df = read_half_ppr_predictions(season, week)
    preds_with_fpoints_df = get_fantasy_points_with_actuals(pred_df, fantasy_points_df)
    actuals_df = read_weekly_actuals(season, week)
    merged_df = merge_preds_actuals(preds_with_fpoints_df, actuals_df)
    diff_df = calculate_differences(merged_df)
    metrics_df = calculate_accuracy_metrics(diff_df, season, week)

    write_predictions_diffs(diff_df)
    write_accuracy_metrics(metrics_df)
