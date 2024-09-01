import polars as pl
import pandas as pd

from jobs.shared.logging_config import logger
from jobs.shared.points_calc import calculate_fantasy_points
from jobs.shared.points_config import PointsConfig, STANDARD_PPR, STANDARD_HALF_PPR, DK_DFS
from jobs.shared.settings import settings


def read_weekly_predictions_base(season: int, week: int) -> pl.DataFrame:
    # Would use pl.read_database_uri but that depends on connectorx which can't run in docker right now
    df = pd.read_sql(
        sql=f"select * from weekly_predictions_base where season = {season} and week = {week}",
        con=settings.POSTGRES_CONN_STRING
    )
    return pl.from_pandas(df)



def calculate_fantasy_points_for_default_configs(df: pl.DataFrame, points_config: PointsConfig) -> pl.DataFrame:
    return df.with_columns(pl.struct('passing_yards', 'passing_tds', 'interceptions', 'receptions',
                                     'receiving_yards','receiving_tds', 'rushing_yards', 'rushing_tds',
                                     'fumbles', 'rushing_2pt_conversions', 'receiving_2pt_conversions',
                                     'passing_2pt_conversions') \
                    .map_elements(
        lambda x: calculate_fantasy_points(points_config, x['passing_yards'], x['passing_tds'],
                                           x['interceptions'], x['receptions'], x['receiving_yards'],
                                           x['receiving_tds'], x['rushing_yards'], x['rushing_tds'],
                                           x['fumbles'], x['rushing_2pt_conversions'], x['receiving_2pt_conversions'],
                                           x['passing_2pt_conversions']),
        return_dtype=pl.Float64).alias('fantasy_points'))


def insert_to_db(df: pl.DataFrame, table_name: str) -> None:
    df = df.select('player_id', 'season', 'week', 'fantasy_points')
    df.write_database(
        table_name=table_name,
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='append'
    )


def main(season: int, week: int):

    logger.info(f'Running fantasy points calculation for season {season} and week {week}')

    default_league_configs = [(STANDARD_PPR, 'weekly_predictions_std_full_ppr'),
                              (STANDARD_HALF_PPR, 'weekly_predictions_std_half_ppr'),
                              (DK_DFS, 'weekly_predictions_dk_dfs')]
    predictions_df = read_weekly_predictions_base(season, week)
    for config in default_league_configs:
        fantasy_points_df = calculate_fantasy_points_for_default_configs(predictions_df, config[0])
        insert_to_db(fantasy_points_df, config[1])
