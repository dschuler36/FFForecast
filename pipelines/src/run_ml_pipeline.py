import argparse

from jobs.data_pulls import weekly_roster_pull
from jobs.ml import train_prediction_model, batch_prediction, create_fantasy_points_default_configs
from jobs.shared.api_utils import get_current_season_week
from jobs.shared.logging_config import logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--override_season_week', action='store_true', help='Override season and week')
    parser.add_argument('--season', type=int, default=None, help='Season number')
    parser.add_argument('--week', type=int, default=None, help='Week number')

    args = parser.parse_args()

    # Check if override_season_week is set to True, then validate season and week
    if args.override_season_week:
        if args.season is None or args.week is None:
            parser.error("--season and --week must be set if --override_season_week is specified")

    return args

if __name__ == '__main__':
    args = parse_args()
    override_season_week = args.override_season_week
    if override_season_week:
        season = args.season
        week = args.week
        logger.info(f'Overriding season/week...')
    else:
        logger.info(f'Calling api to get latest season/week...')
        season, week = get_current_season_week()

    logger.info(f'Running ML prediction pipeline for season: {season} and week {week}')

    weekly_roster_pull.main(season=season, week=week)
    train_prediction_model.main(season=season, week=week)
    batch_prediction.main(season=season, week=week)
    create_fantasy_points_default_configs.main(season=season, week=week)
