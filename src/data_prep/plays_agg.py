import os

import polars as pl

from src.config import config


def read_play_by_play_data() -> pl.DataFrame:
    input_path = config['local']['data_paths']['inputs']['play_by_play']
    return pl.read_parquet(os.path.join(input_path, '*.parquet'))


def subset_plays_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.select('game_id', 'posteam', 'home_team', 'passer', 'passer_id', 'rusher', 'rusher_id', 'receiver',
                     'receiver_id', 'pass', 'rush', 'yards_gained', 'fumble', 'touchdown', 'pass_touchdown',
                     'rush_touchdown', 'rush_attempt', 'pass_attempt', 'yards_after_catch', 'interception')


def filter_to_fantasy_plays(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(~(pl.col('passer').is_null() & pl.col('rusher').is_null() & pl.col('receiver').is_null()))


def create_home_away_col(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(pl.when(df['posteam'] == df['home_team'])
                           .then(pl.lit('home'))
                           .otherwise(pl.lit('away'))
                           .alias('home_away'),
                         df['game_id'].str.split('_').list.get(2).alias('team_1'),
                         df['game_id'].str.split('_').list.get(3).alias('team_2'))
    df = df.with_columns(pl.when(df['posteam'] == df['team_1'])
                           .then(df['team_1']).otherwise(df['team_2'])
                           .alias('opponent'))
    df.drop(['team_1', 'team_2'])
    return df


def reformat_plays_for_position(df: pl.DataFrame) -> pl.DataFrame:
    passers = df.select(['game_id', 'posteam', 'home_away', 'opponent', 'passer', 'passer_id',
                         'yards_gained', 'pass_attempt', 'pass_touchdown', 'fumble', 'interception']) \
                .rename({'passer': 'player',
                         'passer_id': 'player_id',
                         'yards_gained': 'passing_yards',
                         'pass_attempt': 'passing_attempts',
                         'pass_touchdown': 'passing_touchdowns'}) \
                .filter(pl.col('player_id').is_not_null())

    rushers = df.select(['game_id', 'posteam', 'home_away', 'opponent', 'rusher', 'rusher_id',
                         'yards_gained', 'rush_attempt', 'rush_touchdown', 'fumble']) \
                .rename({'rusher': 'player',
                         'rusher_id': 'player_id',
                         'yards_gained': 'rushing_yards',
                         'rush_attempt': 'rushing_attempts',
                         'rush_touchdown': 'rushing_touchdowns'}) \
                .filter(pl.col('player_id').is_not_null())

    receivers = df.select(['game_id', 'posteam', 'home_away', 'opponent', 'receiver', 'receiver_id',
                           'yards_gained', 'touchdown', 'fumble']) \
                  .rename({'receiver': 'player',
                           'receiver_id': 'player_id',
                           'yards_gained': 'receiving_yards',
                           'touchdown': 'receiving_touchdowns'}) \
                  .with_columns(pl.lit(1).alias('receptions')) \
                  .filter(pl.col('player_id').is_not_null())

    return pl.concat([passers, rushers, receivers], how='diagonal')


def agg_plays_to_game_and_player(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by(['game_id', 'posteam', 'home_away', 'opponent', 'player', 'player_id']) \
             .agg(pl.sum('passing_attempts').alias('passing_attempts'),
                  pl.sum('passing_touchdowns').alias('passing_touchdowns'),
                  pl.sum('passing_yards').alias('passing_yards'),
                  pl.sum('rushing_attempts').alias('rushing_attempts'),
                  pl.sum('rushing_yards').alias('rushing_yards'),
                  pl.sum('rushing_touchdowns').alias('rushing_touchdowns'),
                  pl.sum('receptions').alias('receptions'),
                  pl.sum('receiving_yards').alias('receiving_yards'),
                  pl.sum('receiving_touchdowns').alias('receiving_touchdowns'),
                  pl.sum('fumble').alias('fumbles'),
                  pl.sum('interception').alias('interceptions'))


def add_time_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        pl.col('game_id').str.split('_').list.get(0).cast(pl.Int16, strict=False).alias('season'),
        pl.col('game_id').str.split('_').list.get(1).cast(pl.Int8, strict=False).alias('week')
    )


def read_players_data() -> pl.DataFrame:
    input_path = config['local']['data_paths']['inputs']['players']
    return pl.read_parquet(os.path.join(input_path, 'players.parquet'))


def get_player_curr_team(plays: pl.DataFrame, players: pl.DataFrame) -> pl.DataFrame:
    players = players.rename(mapping={'gsis_id': 'player_id'}) \
                     .select('player_id', 'position', 'team_abbr')
    return plays.join(players, on='player_id', how='left') \
                .rename(mapping={'team_abbr': 'curr_team', 'posteam': 'team'})


def write_output(df: pl.DataFrame, run_id: str) -> None:
    output_filename = f'play_by_play_agg_{run_id}.parquet'
    output_file = os.path.join(config['local']['data_paths']['outputs']['play_by_play_agg'], output_filename)
    df.write_parquet(output_file)


def main(run_id):
    plays_df = read_play_by_play_data()
    plays_subset_df = subset_plays_columns(plays_df)
    fantasy_plays_df = filter_to_fantasy_plays(plays_subset_df)
    home_away_df = create_home_away_col(fantasy_plays_df)
    reformatted_df = reformat_plays_for_position(home_away_df)
    agg_plays_df = agg_plays_to_game_and_player(reformatted_df)
    agg_with_week_df = add_time_columns(agg_plays_df)
    players_df = read_players_data()
    agg_plays_with_team = get_player_curr_team(agg_with_week_df, players_df)

    write_output(agg_plays_with_team, run_id)
