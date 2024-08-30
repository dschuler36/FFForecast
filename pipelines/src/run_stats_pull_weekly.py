from jobs.data_pulls import weekly_stats_pull, weekly_accuracy
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('season', type=int)
    parser.add_argument('week', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    season = args.season
    week = args.week
    print(f'Running weekly stats pull for season: {season} and week: {week}')
    weekly_stats_pull.main([season], week)
    weekly_accuracy.main(season, week)
