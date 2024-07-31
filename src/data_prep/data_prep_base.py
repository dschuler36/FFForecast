import pandas as pd


class DataPrep:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = self._read_csv()

    def _read_csv(self):
        return pd.read_csv(self.data_path, header='infer')

