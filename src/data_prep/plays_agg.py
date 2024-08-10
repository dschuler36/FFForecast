from datetime import datetime

import pandas as pd
import polars as pl
import os
from src.config import config


def read_play_by_play_data() -> pd.DataFrame:
    input_path = config['local']['data_paths']['inputs']['play_by_play']
    return pl.read_parquet(os.path.join(input_path, '*.parquet'))


def subset_plays_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.select('game_id', 'posteam', 'home_team', 'passer', 'passer_id', 'rusher', 'rusher_id', 'receiver',
                     'receiver_id', 'pass', 'rush', 'yards_gained', 'fumble', 'touchdown', 'pass_touchdown',
                     'rush_touchdown', 'rush_attempt', 'pass_attempt', 'yards_after_catch', 'interception')


def filter_to_fantasy_plays(df: pl.DataFrame) -> pl.DataFrame:
    return df.drop_nulls(subset=['passer', 'rusher', 'receiver'])


def reformat_plays_for_position(df: pd.DataFrame) -> pd.DataFrame:
    passers = df[['game_id', 'posteam', 'home_away', 'opponent', 'passer', 'passer_id', 'yards_gained', 'pass_attempt',
                  'pass_touchdown', 'fumble', 'interception']].copy()
    passers.rename(columns={'passer': 'player', 'passer_id': 'player_id', 'yards_gained': 'passing_yards',
                            'pass_attempt': 'passing_attempts', 'pass_touchdown': 'passing_touchdowns'}, inplace=True)
    passers = passers.loc[passers['player_id'].notnull()]

    rushers = df[['game_id', 'posteam', 'home_away', 'opponent', 'rusher', 'rusher_id', 'yards_gained', 'rush_attempt',
                  'rush_touchdown', 'fumble']].copy()
    rushers.rename(columns={'rusher': 'player', 'rusher_id': 'player_id', 'yards_gained': 'rushing_yards',
                            'rush_attempt': 'rushing_attempts', 'rush_touchdown': 'rushing_touchdowns'}, inplace=True)
    rushers = rushers.loc[rushers['player_id'].notnull()]

    receivers = df[['game_id', 'posteam', 'home_away', 'opponent', 'receiver', 'receiver_id', 'yards_gained',
                    'touchdown', 'fumble']].copy()
    receivers.rename(columns={'receiver': 'player', 'receiver_id': 'player_id', 'yards_gained': 'receiving_yards',
                              'touchdown': 'receiving_touchdowns'}, inplace=True)
    receivers['receptions'] = 1
    receivers = receivers.loc[receivers['player_id'].notnull()]

    return pd.concat([passers, rushers, receivers], ignore_index=True)


def agg_plays_to_game_and_player(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['game_id', 'posteam', 'home_away', 'opponent', 'player', 'player_id']).agg(
                        passing_attempts=('passing_attempts', 'sum'),
                        passing_yards=('passing_yards', 'sum'),
                        passing_touchdowns=('passing_touchdowns', 'sum'),
                        rushing_attempts=('rushing_attempts', 'sum'),
                        rushing_yards=('rushing_yards', 'sum'),
                        rushing_touchdowns=('rushing_touchdowns', 'sum'),
                        receptions=('receptions', 'sum'),
                        receiving_yards=('receiving_yards', 'sum'),
                        receiving_touchdowns=('receiving_touchdowns', 'sum'),
                        fumbles=('fumble', 'sum'),
                        interceptions=('interception', 'sum')
                       ).reset_index()


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['season'] = df['game_id'].str.split('_').str[0].astype('int')
    df['week'] = df['game_id'].str.split('_').str[1].astype('int')
    return df


def create_home_away_col(df: pl.DataFrame) -> pl.DataFrame:
    df.with_columns('home_away', pl.when(df['posteam'], ))
    df['home_away'] = df.apply(lambda row: 'home' if row['posteam'] == row['home_team'] else 'away', axis=1)
    df['team_1'] = df['game_id'].str.split('_').str[2]
    df['team_2'] = df['game_id'].str.split('_').str[3]
    df['opponent'] = df.apply(lambda row: row['team_1'] if row['posteam'] != row['team_1'] else row['team_2'], axis=1)
    df.drop(['team_1', 'team_2'], axis=1, inplace=True)
    return df


def read_players_data() -> pd.DataFrame:
    input_path = config['local']['data_paths']['inputs']['players']
    return pd.read_parquet(os.path.join(input_path, 'players.parquet'))


def get_player_curr_team(plays: pd.DataFrame, players: pd.DataFrame) -> pd.DataFrame:
    players = players.rename(columns={'gsis_id': 'player_id'})
    return pd.merge(plays, players[['player_id', 'position', 'team_abbr']], on='player_id', how='left') \
             .rename(columns={'team_abbr': 'curr_team', 'posteam': 'team'})


def write_output(df: pd.DataFrame, run_id: str) -> None:
    output_filename = f'play_by_play_agg_{run_id}.parquet'
    output_file = os.path.join(config['local']['data_paths']['outputs']['play_by_play_agg'], output_filename)
    df.to_parquet(output_file, index=False)


def main(run_id):
    pd.options.mode.copy_on_write = True
    plays_df = read_play_by_play_data()
    plays_subset_df = subset_plays_columns(plays_df)
    fantasy_plays_df = filter_to_fantasy_plays(plays_subset_df)
    home_away_df = create_home_away_col(fantasy_plays_df)
    print(fantasy_plays_df)
    reformatted_df = reformat_plays_for_position(home_away_df)
    agg_plays_df = agg_plays_to_game_and_player(reformatted_df)
    agg_with_week_df = add_time_columns(agg_plays_df)

    players_df = read_players_data()
    agg_plays_with_team = get_player_curr_team(agg_with_week_df, players_df)

    write_output(agg_plays_with_team, run_id)
