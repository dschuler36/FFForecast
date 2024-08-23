from typing import List

import polars as pl
import nfl_data_py as nfl

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
                 .agg(pl.max('depth_team').cast(pl.Int8).alias('depth_ranking'))
    if week is not None:
        depth_df = depth_df.filter(pl.col('week') == week)
    return depth_df
