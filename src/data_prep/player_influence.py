import os

import pandas as pd
import polars as pl
from src.config import config
from src.utils.points_calc import calculate_fantasy_points
from src.utils.points_config import PointsConfig, STANDARD_HALF_PPR


def read_pbp_agg(run_id: str) -> pl.DataFrame:
    pbp_agg_path = config['local']['data_paths']['outputs']['play_by_play_agg']
    pbp_filename = f'play_by_play_agg_{run_id}.parquet'
    return pl.read_parquet(os.path.join(pbp_agg_path, pbp_filename))


def read_rosters(run_id: str) -> pl.DataFrame:
    rosters_path = config['local']['data_paths']['outputs']['rosters']
    rosters_filename = f'rosters_{run_id}.parquet'
    return pl.read_parquet(os.path.join(rosters_path, rosters_filename))


def calculate_pbp_fantasy_points(df: pd.DataFrame, pc: PointsConfig) -> pd.DataFrame:
    return df.with_columns(pl.struct('passing_yards', 'passing_touchdowns', 'interceptions', 'receptions',
                                     'receiving_yards', 'receiving_touchdowns', 'rushing_yards', 'rushing_touchdowns',
                                     'fumbles')
                             .map_elements(lambda x: calculate_fantasy_points(STANDARD_HALF_PPR,
                                                                              x['passing_yards'],
                                                                              x['passing_touchdowns'],
                                                                              x['interceptions'],
                                                                              x['receptions'],
                                                                              x['receiving_yards'],
                                                                              x['receiving_touchdowns'],
                                                                              x['rushing_yards'],
                                                                              x['rushing_touchdowns'],
                                                                              x['fumbles']),
                                           return_dtype=pl.Float64).alias('fantasy_points'))


def filter_rosters_to_specific_positions(df: pl.DataFrame) -> pl.DataFrame:
    relevant_positions = ['QB', 'WR', 'RB', 'OL', 'TE']
    return df.filter(df['position'].is_in(relevant_positions))


def create_roster_by_game(pbp_df: pl.DataFrame, roster_df: pl.DataFrame) -> pl.DataFrame:
    joined_df = pbp_df.join(roster_df.select('team', 'week', 'season', 'position', 'full_name', 'player_id', 'active'),
                            on=['team', 'week', 'season']) \
                      .rename(mapping={'player_id_right': 'teammate_id'})

    return joined_df.group_by('game_id', 'player_id', 'teammate_id', 'position') \
                    .agg(pl.max('active').alias('active'))


def collect_teammates_as_list(df):
    active_teammates = df.filter(pl.col('active') == 1).get_column('teammate_id').to_list()
    return pl.struct({
        'active_teammates': active_teammates,
        'num_active_teammates': len(active_teammates)
    })


def create_teammate_active_columns(df):
    reshaped_teammate_presence = df.pivot(
        values="active",
        index=["game_id", "player_id"],
        columns="teammate_id",
        aggregate_function="first"
    )

    # Rename columns to add 'teammate_' prefix
    new_column_names = {
        col: f"teammate_{col}"
        for col in reshaped_teammate_presence.columns
        if col not in ["game_id", "player_id"]
    }
    reshaped_teammate_presence = reshaped_teammate_presence.rename(new_column_names)

    # Fill null values with 0
    reshaped_teammate_presence = reshaped_teammate_presence.fill_null(0)

    # Convert float values to int for teammate columns
    for col in reshaped_teammate_presence.columns:
        if col.startswith('teammate_'):
            reshaped_teammate_presence = reshaped_teammate_presence.with_columns(
                pl.col(col).cast(pl.Int32)
            )

    return reshaped_teammate_presence


def main(run_id):
    pbp_agg_df = read_pbp_agg(run_id)
    rosters_df = read_rosters(run_id)
    fantasy_points_df = calculate_pbp_fantasy_points(pbp_agg_df, STANDARD_HALF_PPR)
    filtered_rosters_df = filter_rosters_to_specific_positions(rosters_df)
    roster_by_game_df = create_roster_by_game(pbp_agg_df, filtered_rosters_df)
    df_with_teammate_active_flag = create_teammate_active_columns(roster_by_game_df)
    print(df_with_teammate_active_flag)
    print(fantasy_points_df)