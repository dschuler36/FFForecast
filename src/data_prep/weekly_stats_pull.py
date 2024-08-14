from typing import List

import polars as pl
import nfl_data_py as nfl


def pull_nfl_data(seasons: List[int], week: int = None) -> pl.DataFrame:
    nfl_df = pl.from_pandas(nfl.import_weekly_data(seasons))
    if week is not None:
        nfl_df = nfl_df.filter(pl.col('week') == week)
    return nfl_df


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



def select_output_cols(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        'player_id', 'player_display_name', 'position', 'headshot_url', 'recent_team', 'season', 'week',
        'opponent_team', 'completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions', 'fumbles', 'sacks',
        'sack_yards', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 'passing_epa',
        'passing_2pt_conversions', 'pacr', 'dakota', 'carries', 'rushing_yards', 'rushing_tds', 'rushing_first_downs',
        'rushing_epa', 'rushing_2pt_conversions', 'receptions', 'targets', 'receiving_yards', 'receiving_tds',
        'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_epa',
        'receiving_2pt_conversions', 'racr', 'target_share', 'air_yards_share', 'wopr', 'special_teams_tds',
        'fantasy_points', 'fantasy_points_ppr'
    )


def insert_to_db(df: pl.DataFrame) -> None:
    df.write_database(
        table_name='weekly_stats',
        connection='postgresql://ff:ff@0.0.0.0:5432/ff',
        if_table_exists='append'
    )

def main(seasons: List[int], week: int = None):
    nfl_df = pull_nfl_data(seasons, week)
    fantasy_df = filter_down_to_fantasy_positions(nfl_df)
    combined_fumble_df = combine_fumble_columns(fantasy_df)
    final_df = select_output_cols(combined_fumble_df)
    insert_to_db(final_df)


if __name__ == '__main__':
    main([2020, 2021, 2022, 2023])