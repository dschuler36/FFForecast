import argparse

from jobs.data_pulls import weekly_roster_pull
from jobs.ml import train_prediction_model, batch_prediction, create_fantasy_points_default_configs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('season', type=int)
    parser.add_argument('week', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    season = args.season
    week = args.week

    print(f'Running ML prediction pipeline for season: {season} and week {week}')

    weekly_roster_pull.main(season=season, week=week)
    train_prediction_model.main(season=season, week=week)
    batch_prediction.main(season=season, week=week)
    create_fantasy_points_default_configs.main(season=season, week=week)
