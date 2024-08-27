import numpy as np
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder

from jobs.shared.constants import cat_features, model_prediction_vars, numerical_features
from jobs.shared.logging_config import logger
from jobs.shared.settings import settings

def read_weekly_stats() -> pd.DataFrame:
    return pd.read_sql(
        sql='select * from weekly_stats;',
        con=settings.POSTGRES_CONN_STRING
    )

def create_preprocessor(cat_features_to_encode):
    return ColumnTransformer(
        transformers=[
            ('cat_features', OneHotEncoder(sparse_output=True, handle_unknown='ignore'), cat_features_to_encode)
        ],
        remainder='passthrough'
    )

def train_model(df: pd.DataFrame):
    # Sort data by season and week to maintain temporal order
    df = df.sort_values(by=['season', 'week'])

    # Initialize the preprocessor
    preprocessor = create_preprocessor(cat_features)

    # Prepare the feature matrix and target variable
    X = df[cat_features + numerical_features]
    y = df[model_prediction_vars]

    # Fit the preprocessor on the entire dataset
    X_preprocessed = preprocessor.fit_transform(X)

    # Create a weight vector based on week and season
    # More recent weeks get higher weight, and recent seasons can be scaled similarly
    df['week_weight'] = np.exp(df['week'] / df['week'].max())
    df['season_weight'] = df['season'] / df['season'].max()

    # Combine weights
    sample_weights = df['week_weight'] * df['season_weight']

    # Define the seasons for manual splits
    season_splits = {
        1: (df['season'] <= 2020, df['season'] == 2021),
        2: (df['season'] <= 2021, df['season'] == 2022),
        3: (df['season'] <= 2022, df['season'] == 2023),
    }

    mse_scores = []
    mae_scores = []

    # Perform cross-validation based on season splits with sample weighting
    for split_id, (train_condition, test_condition) in season_splits.items():
        X_train = X_preprocessed[train_condition]
        y_train = y[train_condition]
        sample_weights_train = sample_weights[train_condition]

        X_test = X_preprocessed[test_condition]
        y_test = y[test_condition]

        # Initialize and train the model with sample weights
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train, sample_weight=sample_weights_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate errors
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse_scores.append(mse)
        mae_scores.append(mae)

        logger.info(f"Season {split_id} - MSE: {mse}, MAE: {mae}")

    # Average the scores across seasons
    avg_mse = np.mean(mse_scores)
    avg_mae = np.mean(mae_scores)

    logger.info(f"Average MSE: {avg_mse}")
    logger.info(f"Average MAE: {avg_mae}")

    # Fit the final model on all data up to the latest available season
    model.fit(X_preprocessed, y, sample_weight=sample_weights)

    return model, preprocessor

def save_model_and_preprocessor(model, preprocessor, model_filename, preprocessor_filename):
    joblib.dump(model, model_filename)
    joblib.dump(preprocessor, preprocessor_filename)

def main(season: int, week: int):

    logger.info(f'Running weekly_stats_pull for season {season} and week {week}')

    df = read_weekly_stats()
    model, preprocessor = train_model(df)
    model_filename = settings.FF_PREDICTION_MODEL_FILE.format(season=season, week=week)
    preprocessor_filename = settings.FF_PREDICTION_PREPROCESSOR_FILE.format(season=season, week=week)
    save_model_and_preprocessor(model, preprocessor, model_filename, preprocessor_filename)
