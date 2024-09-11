from typing import List

import nfl_data_py as nfl
import pandas as pd
import polars as pl
from sqlalchemy import create_engine, MetaData, Table, delete

from jobs.shared.constants import positions
from jobs.shared.logging_config import logger
from jobs.shared.settings import settings


def pull_schedules(season: int, week: int = None) -> pl.DataFrame:
    df =  pl.from_pandas(nfl.import_schedules([season])) \
            .drop('nfl_detail_id')
    if week is not None:
        df = df.filter(pl.col('week') == week)
    return df


def pull_depth_chart(seasons: List[int], week: int) -> pl.DataFrame:

    # TODO: temp workaround for week 1 - remove at some point
    if len(seasons) == 1 and seasons[0] == 2024 and week == 1:
        depth_df = pl.from_pandas(pd.read_sql(
            sql=f'select * from depth_chart_tmp where season = {seasons[0]} and week = {week}',
            con=settings.POSTGRES_CONN_STRING
        ))
        depth_df = depth_df.select('season', pl.col('team').alias('club_code'), 'week',
                                   pl.col('player_id').alias('gsis_id'), 'position',
                                   pl.col('depth').alias('depth_ranking'))
    else:
        depth_df = pl.from_pandas(nfl.import_depth_charts(seasons)) \
                     .filter(pl.col('position').is_in(positions)) \
                     .filter(pl.col('position') == pl.col('depth_position')) \
                     .select('season', 'club_code', 'week', 'depth_team', 'gsis_id', 'position') \
                     .unique() \
                     .group_by(['season', 'club_code', 'week', 'gsis_id', 'position']) \
                     .agg(pl.max('depth_team').cast(pl.Int8).alias('depth_ranking'))
        if week is not None:
            depth_df = depth_df.filter(pl.col('week') == week)

    return depth_df


def pull_roster(seasons: List[int], week: int) -> pl.DataFrame:
    # Have to pull one week at a time and concat due to bug: https://github.com/nflverse/nfl_data_py/issues/75
    nfl_df = None
    for index, season in enumerate(seasons):
        # Columns' dtypes change throughout time so aligning them all to current version
        tmp_df = pl.from_pandas(nfl.import_weekly_rosters([season])) \
                   .with_columns(pl.col('years_exp').cast(pl.Int32)) \
                   .with_columns(pl.col('entry_year').cast(pl.Int32)) \
                   .with_columns(pl.col('weight').cast(pl.Float64))

        if index == 0:
            nfl_df = tmp_df
        else:
            nfl_df = pl.concat(items=[nfl_df, tmp_df])

    if week is not None:
        nfl_df = nfl_df.filter(pl.col('week') == week)

        if len(nfl_df) == 0:
            raise ValueError(f'No weekly roster data found for season {seasons} and week {week}')

    return nfl_df


def pull_schedule(seasons: List[int], week: int) -> pl.DataFrame:
    schedule_df = None
    for index, season in enumerate(seasons):
        tmp_df = pull_schedules(season, week)
        if index == 0:
            schedule_df = tmp_df
        else:
            schedule_df = pl.concat(items=[schedule_df, tmp_df])

    if week is not None:
        schedule_df = schedule_df.filter(pl.col('week') == week)

    return schedule_df


def pull_stats_agg(seasons: List[int], week: int = None) -> pl.DataFrame:
    nfl_df = pl.from_pandas(nfl.import_weekly_data(seasons))
    if week is not None:
        nfl_df = nfl_df.filter(pl.col('week') == week)
    return nfl_df


def upsert_to_db(df: pl.DataFrame, table_name: str, season: int, week: int) -> None:
    # Have to delete data for the season / week then insert
    # otherwise, someone who was injured will remain in the predictions from old data
    engine = create_engine(settings.POSTGRES_CONN_STRING)
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    with engine.begin() as conn:
        stmt = (
            delete(table)
            .where(
                (table.c.season == season) &
                (table.c.week == week)
            )
        )

        logger.info(f'Deleting data for season {season} and week {week} from {table_name}')
        conn.execute(stmt)

    logger.info(f'Inserting data for season {season} and week {week} to {table_name}')
    df.write_database(
        table_name=table_name,
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='append'
    )