from typing import List

import polars as pl
import nfl_data_py as nfl


def pull_nfl_data(seasons: List[int], week: int = None) -> pl.DataFrame:
    nfl_df = pl.from_pandas(nfl.import_weekly_rosters(seasons))
    if week is not None:
        nfl_df = nfl_df.filter(pl.col('week') == week)
    return nfl_df

if __name__ == '__main__':
    df = pull_nfl_data([2023])
    print(df.filter(pl.col('player_id') == '00-0033930'))