from typing import List

import polars as pl

from jobs.shared.data_access import pull_depth_chart, pull_roster, pull_schedule, pull_stats_agg
from jobs.shared.logging_config import logger
from jobs.shared.settings import settings


def filter_down_to_fantasy_positions(df: pl.DataFrame) -> pl.DataFrame:
    positions = ['FB', 'TE', 'QB', 'WR', 'RB']
    return df.filter(pl.col('position').is_in(positions)) \
             .with_columns(pl.when(pl.col('position') == 'FB')
                                          .then(pl.lit('RB'))
                                          .otherwise(pl.col('position'))
                                          .alias('position'))


def combine_fumble_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns((pl.col('sack_fumbles_lost') +
                            pl.col('rushing_fumbles_lost') +
                            pl.col('receiving_fumbles_lost')).alias('fumbles'))


def join_with_schedule_df(stats_df: pl.DataFrame, sched_df: pl.DataFrame):
    stats_df = stats_df.with_columns([
        pl.col("season").cast(pl.Int64),
        pl.col("week").cast(pl.Int64)
    ])

    sched_df = sched_df.with_columns([
        pl.col("season").cast(pl.Int64),
        pl.col("week").cast(pl.Int64)
    ])

    merged_df = stats_df.join(
        sched_df,
        left_on=["season", "week", "recent_team"],
        right_on=["season", "week", "home_team"],
        how="left"
    ).with_columns(
        pl.lit("home").alias("home_away")
    ).join(
        sched_df,
        left_on=["season", "week", "recent_team"],
        right_on=["season", "week", "away_team"],
        how="left"
    ).with_columns(
        pl.when(pl.col("home_away").is_null())
          .then(pl.lit("away"))
          .otherwise(pl.col("home_away"))
          .alias("home_away")
    )
    return merged_df


def join_stats_with_depth_chart(stats_df: pl.DataFrame, depth_df: pl.DataFrame) -> pl.DataFrame:
    depth_df = depth_df.select(pl.col('gsis_id').alias('player_id'),
                               'depth_ranking',
                               pl.col('week').cast(pl.Int64).alias('week'),
                               pl.col('season').cast(pl.Int64).alias('season'))
    return stats_df.join(depth_df, on=['player_id', 'week', 'season'])


def join_stats_with_roster(stats_df: pl.DataFrame, roster_df: pl.DataFrame) -> pl.DataFrame:
    join_keys = ['season', 'week', 'player_id']
    roster_df = roster_df.with_columns(pl.col('season').cast(pl.Int64)) \
                         .with_columns(pl.col('week').cast(pl.Int64)) \
                         .select(*join_keys, 'age')
    return stats_df.join(roster_df, on=join_keys)



def select_output_cols(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        'player_id', 'player_display_name', 'position', 'headshot_url', pl.col('recent_team').alias('team'),
        'season', 'week', pl.col('opponent_team').alias('opponent'), 'home_away', 'age', 'completions', 'attempts',
        'passing_yards', 'passing_tds', 'interceptions', 'fumbles', 'sacks',
        'sack_yards', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 'passing_epa',
        'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards', 'rushing_tds', 'rushing_first_downs',
        'rushing_epa', 'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards', 'receiving_tds',
        'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_epa',
        'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share', 'wopr', 'special_teams_tds',
        'depth_ranking', 'fantasy_points', 'fantasy_points_ppr'
    )


def insert_to_db(df: pl.DataFrame) -> None:
    df.write_database(
        table_name='weekly_stats',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='append'
    )

def main(seasons: List[int], week: int = None):

    logger.info(f'Running weekly_stats_pull for season {seasons} and week {week}')

    stats_df = pull_stats_agg(seasons, week)
    schedule_df = pull_schedule(seasons, week)
    fantasy_df = filter_down_to_fantasy_positions(stats_df)
    combined_fumble_df = combine_fumble_columns(fantasy_df)
    merged_df = join_with_schedule_df(combined_fumble_df, schedule_df)
    depth_df = pull_depth_chart(seasons, week)
    stats_with_depth_df = join_stats_with_depth_chart(merged_df, depth_df)

    roster_df = pull_roster(seasons, week)
    stats_with_age_df = join_stats_with_roster(stats_with_depth_df, roster_df)

    final_df = select_output_cols(stats_with_age_df)
    insert_to_db(final_df)
