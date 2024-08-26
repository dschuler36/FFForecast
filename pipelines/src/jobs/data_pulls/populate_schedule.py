from jobs.shared.data_access import pull_schedule
import polars as pl

from jobs.shared.settings import settings


def select_output_cols(df: pl.DataFrame) -> pl.DataFrame:
    return df.select('game_id', 'season', 'week', pl.col('gameday').cast(pl.Date),
                     'gametime', 'weekday', 'home_team', 'away_team')


def insert_to_db(df: pl.DataFrame) -> None:
    df.write_database(
        table_name='schedule',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='replace'
    )


def main(season: int):
    schedule_df = pull_schedule([season], None)
    output_df = select_output_cols(schedule_df)
    insert_to_db(output_df)
