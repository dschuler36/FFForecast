import joblib
import pandas as pd
import polars as pl

from jobs.shared.constants import cat_features, model_prediction_vars, numerical_features
from jobs.shared.settings import settings


def read_weekly_roster(season: int, week: int) -> pd.DataFrame:
    return pd.read_sql(
        sql=f'select * from weekly_roster where season = {season} and week = {week}',
        con=settings.POSTGRES_CONN_STRING
    )


def load_model_and_preprocessor(model_filename, preprocessor_filename):
    model = joblib.load(model_filename)
    preprocessor = joblib.load(preprocessor_filename)
    return model, preprocessor


def create_predictions(df: pd.DataFrame, model, preprocessor):
    preprocessed_df = preprocessor.transform(df)
    return model.predict(preprocessed_df)


def format_predictions(y_pred, X_test, target_variables):
    # Convert predictions to a DataFrame
    pred_df = pd.DataFrame(y_pred, columns=target_variables)

    # Add player_id (and any other relevant identifier columns) from X_test
    pred_df['player_id'] = X_test['player_id'].reset_index(drop=True)

    # Reorder columns to have identifiers first
    identifier_cols = ['player_id']  # Adjust as needed
    stat_cols = [col for col in pred_df.columns if col not in identifier_cols]
    pred_df = pred_df[identifier_cols + stat_cols]

    return pred_df


def create_final_predictions_df(pred_df: pd.DataFrame, roster_df: pd.DataFrame, season: int, week: int) -> pd.DataFrame:
    pred_df['season'] = season
    pred_df['week'] = week
    joined = pred_df.merge(roster_df[['player_id', 'player_name', 'team', 'opponent', 'position']], on='player_id')
    return joined


def insert_to_db(df: pd.DataFrame) -> None:
    pl_df = pl.from_pandas(df)
    pl_df.write_database(
        table_name='weekly_predictions_base',
        connection=settings.POSTGRES_CONN_STRING,
        if_table_exists='replace'
    )


def main(season: int, week: int):
    df = read_weekly_roster(season, week)
    subset_df = df[cat_features + numerical_features]
    model_filename = settings.FF_PREDICTION_MODEL_FILE.format(season=season, week=week)
    preprocessor_filename = settings.FF_PREDICTION_PREPROCESSOR_FILE.format(season=season, week=week)
    model, preprocessor = load_model_and_preprocessor(model_filename, preprocessor_filename)
    predictions = create_predictions(subset_df, model, preprocessor)
    formatted_predictions = format_predictions(predictions, subset_df, model_prediction_vars)
    final_df = create_final_predictions_df(formatted_predictions, df, season, week)
    insert_to_db(final_df)
