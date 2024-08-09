import pandas as pd
import os
from src.config import config


def read_roster_data() -> pd.DataFrame:
    input_path = config['local']['data_paths']['inputs']['rosters']
    years_to_process = ['2020', '2021', '2022', '2023']
    df = None
    for year in years_to_process:
        path = os.path.join(input_path, f'roster_weekly_{year}.parquet')
        tmp_df = pd.read_parquet(path)
        df = pd.concat([df, tmp_df])
    return df


def filter_to_active_players(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df['status'] == 'ACT']


def prep_final_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df['week'] = df.week.astype(int, copy=False)
    df.rename(columns={'gsis_id': 'player_id'}, inplace=True)
    return df[['season', 'team', 'position', 'status', 'full_name', 'birth_date', 'height', 'weight', 'player_id',
               'week', 'game_type', 'entry_year', 'draft_club', 'draft_number']]


def write_output(df: pd.DataFrame) -> None:
    output_file = os.path.join(config['local']['data_paths']['outputs']['rosters'], 'rosters.parquet')
    df.to_parquet(output_file, index=False)


if __name__ == '__main__':
    roster_df = read_roster_data()
    active_roster_df = filter_to_active_players(roster_df)
    final_df = prep_final_dataset(active_roster_df)
    write_output(final_df)
