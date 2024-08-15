import pandas as pd
import polars as pl
import pickle
# read weekly roster from pg
# serialize .pkl model
# perform predictions
# write predictions to pg


def read_weekly_roster(season: int, week: int) -> pd.DataFrame:
    return pd.read_sql(
        sql=f'select * from weekly_roster where season = {season} and week = {week}',
        con='postgresql://ff:ff@0.0.0.0:5432/ff'
    )


def serialize_model(model_path: str):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def create_predictions(df: pd.DataFrame, model):
    input_cols = ['player_id', 'team', 'opponent']
    encoded_inputs_df = pd.get_dummies(df, columns=input_cols)
    print(encoded_inputs_df)
    preds = model.predict(encoded_inputs_df)
    return preds


def main(season: int, week: int):
    df = read_weekly_roster(season, week)
    model_file = f'../ff_pred_{season}_{week}.pkl'
    model = serialize_model(model_file)
    predictions = create_predictions(df, model)
    print(predictions)


if __name__ == '__main__':
    main(2023, 1)
