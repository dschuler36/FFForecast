from src.prediction_workflow.ml import train_model
from src.prediction_workflow.data_pulls import weekly_roster_pull

if __name__ == '__main__':
    season = 2023
    week = 1
    # TODO: run this on a separate cadence? only needs to refresh on Tuesdays after MNF.
    # weekly_stats_pull.main(seasons=season, week=week)
    weekly_roster_pull.main(season=season, week=week)
    train_model.main(season=season, week=week)
