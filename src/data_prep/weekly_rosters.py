import os

import polars as pl

from src.config import config


def read_roster_data() -> pl.DataFrame:
    input_path = config['local']['data_paths']['inputs']['rosters']
    return pl.read_parquet(os.path.join(input_path, '*.parquet'))


def create_active_flag(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(pl.when(df['status'] == 'ACT').then(1).otherwise(0).alias('active'))


def prep_final_dataset(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(df['week'].cast(pl.Int8),
                           df['season'].cast(pl.Int16)) \
             .rename(mapping={'gsis_id': 'player_id'}) \
             .select(['season', 'team', 'position', 'status', 'active', 'full_name', 'birth_date', 'height', 'weight',
                      'player_id', 'week', 'game_type', 'entry_year', 'draft_club', 'draft_number'])


def write_output(df: pl.DataFrame, run_id) -> None:
    output_file = os.path.join(config['local']['data_paths']['outputs']['rosters'], f'rosters_{run_id}.parquet')
    df.write_parquet(output_file)


def main(run_id):
    roster_df = read_roster_data()
    active_roster_df = create_active_flag(roster_df)
    final_df = prep_final_dataset(active_roster_df)
    write_output(final_df, run_id)
