import polars as pl
import nfl_data_py as nfl


def pull_schedules(season: int, week: int = None) -> pl.DataFrame:
    df =  pl.from_pandas(nfl.import_schedules([season])) \
            .drop('nfl_detail_id')
    if week is not None:
        df = df.filter(pl.col('week') == week)
    return df
