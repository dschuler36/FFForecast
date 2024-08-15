import argparse

from pipelines.jobs.data_pulls import weekly_stats_pull

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('seasons', type=int, nargs='+')
    return parser.parse_args()





if __name__ == '__main__':
    args = parse_args()
    seasons = args.seasons
    print(f'Running historical stats pull for seasons {seasons}')
    week = None
    weekly_stats_pull.main(seasons, week)
