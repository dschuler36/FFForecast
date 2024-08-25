import argparse

from jobs.data_pulls import populate_schedule


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('season', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    season = args.season
    print(f'Running populate schedule for season {season}')
    populate_schedule.main(season)
