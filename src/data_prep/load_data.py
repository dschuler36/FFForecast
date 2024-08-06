from src.config import config
import duckdb

def load_data():
    config_paths = config['data_paths']
    duckdb.read_parquet(config_paths.values())


if __name__ == '__main__':
    load_data()