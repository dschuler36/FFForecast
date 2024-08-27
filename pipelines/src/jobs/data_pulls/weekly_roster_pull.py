import pandas as pd
import polars as pl

from jobs.shared.constants import positions
from jobs.shared.data_access import pull_schedules, pull_depth_chart, pull_roster
from jobs.shared.logging_config import logger
from jobs.shared.settings import settings


def read_stadium_details() -> pl.DataFrame:
    df = pd.read_sql(
        sql=f'select * from stadium_details',
        con=settings.POSTGRES_CONN_STRING
    )
    return pl.from_pandas(df)


def filter_depth_chart(df: pl.DataFrame) -> pl.DataFrame:
    qbs = df.filter(pl.col('position') == 'QB') \
            .filter(pl.col('depth_ranking') <= 1)

    rbs = df.filter(pl.col('position') == 'RB') \
            .filter(pl.col('depth_ranking') <= 3)

    wrs = df.filter(pl.col('position') == 'WR') \
            .filter(pl.col('depth_ranking') <= 4)

    tes = df.filter(pl.col('position') == 'TE') \
            .filter(pl.col('depth_ranking') <= 2)

    return pl.concat(items=[qbs, rbs, wrs, tes])


def join_stadium_details_to_roster_data(roster_df: pl.DataFrame, stadium_df: pl.DataFrame) -> pl.DataFrame:
    return roster_df.join(stadium_df.drop('stadium_name', 'home_team'), on='stadium_id')


def filter_to_active_players(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col('status') == 'ACT') \
             .filter(pl.col('position').is_in(positions))


def join_roster_with_depth_chart(roster_df: pl.DataFrame, depth_df: pl.DataFrame) -> pl.DataFrame:
    depth_df = depth_df.select('gsis_id', 'depth_ranking')
    return roster_df.join(depth_df, left_on='player_id', right_on='gsis_id', how='inner')


def join_roster_with_schedule(roster_df: pl.DataFrame, opponents_df: pl.DataFrame) -> pl.DataFrame:
    matchups_df = opponents_df.select(['home_team', 'away_team'])
    matchups2_df = matchups_df.rename({'home_team': 'home_team_2', 'away_team': 'away_team_2'})

    return roster_df.join(matchups_df, left_on='team', right_on='home_team', how='left') \
                    .join(matchups2_df, left_on='team', right_on='away_team_2', how='left') \
                    .with_columns(pl.when(pl.col('away_team').is_null())
                                    .then(pl.col('home_team_2'))
                                    .otherwise(pl.col('away_team'))
                                    .alias('opponent')) \
                    .with_columns(pl.when(pl.col('away_team').is_null())
                                    .then(pl.lit('away'))
                                    .otherwise(pl.lit('home'))
                                    .alias('home_away')) \
                    .drop('away_team', 'home_team_2')


def select_output_cols(df: pl.DataFrame) -> pl.DataFrame:
    return df.select('season', 'week', 'position', 'status', 'player_id', 'player_name', 'age', 'team',
                     'opponent', 'home_away', 'depth_ranking')


def insert_to_db(df: pl.DataFrame) -> None:
    df.write_database(
        table_name='weekly_roster',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='replace'
    )

def main(season: int, week: int):

    logger.info(f'Running weekly_roster_pull for season {season} and week {week}')

    # weekly roster prep
    weekly_roster_df = pull_roster([season], week)
    active_players_df = filter_to_active_players(weekly_roster_df)

    # depth chart prep
    depth_df = pull_depth_chart([season], week)
    top_depth_df = filter_depth_chart(depth_df)

    # opponent prep
    opponent_df = pull_schedules(season, week)
    stadium_details_df = read_stadium_details()
    opponent_with_stadium_df = join_stadium_details_to_roster_data(opponent_df, stadium_details_df)

    # combine them
    roster_filtered_by_depth_df = join_roster_with_depth_chart(active_players_df, top_depth_df)
    roster_with_opponent_df = join_roster_with_schedule(roster_filtered_by_depth_df, opponent_with_stadium_df)
    output_df = select_output_cols(roster_with_opponent_df)
    insert_to_db(output_df)
