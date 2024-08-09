import os

import pandas as pd
from src.config import config
from src.utils.points_calc import calculate_fantasy_points
from src.utils.points_config import PointsConfig, STANDARD_HALF_PPR


def read_pbp_agg(run_id: str) -> pd.DataFrame:
    pbp_agg_path = config['local']['data_paths']['outputs']['play_by_play_agg']
    pbp_filename = f'play_by_play_agg_{run_id}.parquet'
    return pd.read_parquet(os.path.join(pbp_agg_path, pbp_filename))


def read_rosters(run_id: str) -> pd.DataFrame:
    rosters_path = config['local']['data_paths']['outputs']['rosters']
    rosters_filename = f'rosters_{run_id}.parquet'
    return pd.read_parquet(os.path.join(rosters_path, rosters_filename))


def calculate_pbp_fantasy_points(df: pd.DataFrame, pc: PointsConfig) -> pd.DataFrame:
    df['fantasy_points'] = df.apply(lambda x: calculate_fantasy_points(pc, x.passing_yards, x.passing_touchdowns,
                                                                       x.interceptions, x.receptions, x.receiving_yards,
                                                                       x.receiving_touchdowns, x.rushing_yards,
                                                                       x.rushing_touchdowns, x.fumbles), axis=1)
    return df


if __name__ == '__main__':
    run_id = '20240809'
    pbp_agg_df = read_pbp_agg(run_id)
    rosters_df = read_rosters(run_id)
    fantasy_points_df = calculate_pbp_fantasy_points(pbp_agg_df, STANDARD_HALF_PPR)


