from typing import List

import nfl_data_py as nfl
import polars as pl

from jobs.shared.constants import positions


def pull_schedules(season: int, week: int = None) -> pl.DataFrame:
    df =  pl.from_pandas(nfl.import_schedules([season])) \
            .drop('nfl_detail_id')
    if week is not None:
        df = df.filter(pl.col('week') == week)
    return df


def pull_depth_chart(seasons: List[int], week: int) -> pl.DataFrame:
    depth_df = pl.from_pandas(nfl.import_depth_charts(seasons)) \
                 .filter(pl.col('position').is_in(positions)) \
                 .filter(pl.col('position') == pl.col('depth_position')) \
                 .select('season', 'club_code', 'week', 'depth_team', 'gsis_id', 'position') \
                 .unique() \
                 .group_by(['season', 'club_code', 'week', 'gsis_id', 'position']) \
                 .agg(pl.max('depth_team').cast(pl.Int8).alias('depth_ranking')) \
                 .rename(mapping={'gsis_id': 'player_id'})
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


def fallback_week(season: int, week: int):
    if week != 1:
        return season, week - 1
    else:
        return season - 1, 16