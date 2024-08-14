import polars as pl
import pickle
# read weekly roster from pg
# serialize .pkl model
# perform predictions
# write predictions to pg


def read_weekly_roster(season: int, week: int):
    return pl.read_database_uri(
        query=f'select * from weekly_roster where season = {season} and week = {week}',
        uri='postgresql://ff:ff@0.0.0.0:5432/ff'
    )

def serialize_model(model_path: str):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def create_predictions(df: pl.DataFrame, model):
    input_df = df.select('player_id', 'team', 'opponent')
    preds = model.predict(input_df)
    return preds


def main(season: int, week: int):
    df = read_weekly_roster(season, week)
    print(df)
    model_file = f'./ff_pred_{season}_{week}.pkl'
    model = serialize_model(model_file)
    predictions = create_predictions(df, model)
    print(predictions)


if __name__ == '__main__':
    main(2023, 1)
