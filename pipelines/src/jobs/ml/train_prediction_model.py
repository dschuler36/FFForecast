import logging

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from mlflow.models.signature import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from jobs.shared.constants import cat_features, model_prediction_vars, numerical_features
from jobs.shared.logging_config import logger
from jobs.shared.settings import settings


def read_weekly_stats() -> pd.DataFrame:
    return pd.read_sql(
        sql='select * from weekly_stats;',
        con=settings.POSTGRES_CONN_STRING
    )

# def create_preprocessor(cat_features_to_encode):
#     return ColumnTransformer(
#         transformers=[
#             ('cat_features', OneHotEncoder(sparse_output=True, handle_unknown='ignore'), cat_features_to_encode)
#         ],
#         remainder='passthrough'
#     )


class EnsembleModel:
    def __init__(self, models):
        self.models = models

    def fit(self, X, y, sample_weight=None):
        # The individual models are already fitted, so we don't need to do anything here
        pass

    def predict(self, X):
        # Make predictions with each model
        predictions = np.array([model.predict(X) for model in self.models])
        print(self.models)

        # Calculate weights based on the model's position in the list (more recent models get higher weights)
        weights = np.linspace(0.5, 1, len(self.models))
        weights = weights / np.sum(weights)

        # Compute weighted average of predictions
        weighted_predictions = np.average(predictions, axis=0, weights=weights)

        return weighted_predictions


# def train_model_with_historical_iterations(df: pd.DataFrame, current_season: int, current_week: int, experiment_name: str):
#
#     # Set up MLflow experiment
#     mlflow.set_experiment(experiment_name)
#
#     # Start an MLflow run
#     with mlflow.start_run(run_name=f"Season_{current_season}_Week_{current_week}"):
#         # Sort data by season and week to maintain temporal order
#         df = df.sort_values(by=['season', 'week'])
#
#         # Initialize the preprocessor
#         preprocessor = create_preprocessor(cat_features)
#
#         # Prepare the feature matrix and target variable
#         X = df[cat_features + numerical_features]
#         y = df[model_prediction_vars]
#
#         # Fit the preprocessor on the entire dataset
#         X_preprocessed = preprocessor.fit_transform(X)
#
#         # Create a weight vector based on week and season
#         df['week_weight'] = np.exp(df['week'] / df['week'].max())
#         df['season_weight'] = df['season'] / df['season'].max()
#         sample_weights = df['week_weight'] * df['season_weight']
#
#         models = []
#         mse_scores = []
#         mae_scores = []
#
#         # Group data by season
#         seasons = df['season'].unique()
#         completed_seasons = seasons[seasons < current_season]
#
#         # Part 1: Train and validate on completed seasons
#         for i in range(1, len(completed_seasons)):
#             train_seasons = completed_seasons[:i]
#             val_season = completed_seasons[i]
#
#             train_mask = df['season'].isin(train_seasons)
#             train_X = X_preprocessed[train_mask]
#             train_y = y[train_mask]
#             train_weights = sample_weights[train_mask]
#
#             val_mask = df['season'] == val_season
#             val_X = X_preprocessed[val_mask]
#             val_y = y[val_mask]
#
#             model = RandomForestRegressor(n_estimators=100, random_state=42)
#             model.fit(train_X, train_y, sample_weight=train_weights)
#
#             y_pred = model.predict(val_X)
#             mse = mean_squared_error(val_y, y_pred)
#             mae = mean_absolute_error(val_y, y_pred)
#
#             mlflow.log_metric(f"MSE_season_{val_season}", mse)
#             mlflow.log_metric(f"MAE_season_{val_season}", mae)
#
#             mse_scores.append(mse)
#             mae_scores.append(mae)
#             models.append(model)
#
#             logger.info(f"Validation on Completed Season {val_season} - MSE: {mse}, MAE: {mae}")
#
#         # Part 2: Train and validate on the current season week by week
#         current_season_data = df[df['season'] == current_season]
#         for week in range(2, current_week + 1):  # Start from week 2 to have at least one week for training
#             train_mask = (df['season'] < current_season) | ((df['season'] == current_season) & (df['week'] < week))
#             train_X = X_preprocessed[train_mask]
#             train_y = y[train_mask]
#             train_weights = sample_weights[train_mask]
#
#             val_mask = (df['season'] == current_season) & (df['week'] == week)
#             val_X = X_preprocessed[val_mask]
#             val_y = y[val_mask]
#
#             model = RandomForestRegressor(n_estimators=100, random_state=42)
#             model.fit(train_X, train_y, sample_weight=train_weights)
#
#             y_pred = model.predict(val_X)
#             mse = mean_squared_error(val_y, y_pred)
#             mae = mean_absolute_error(val_y, y_pred)
#
#             mlflow.log_metric(f"MSE_week_{week}", mse)
#             mlflow.log_metric(f"MAE_week_{week}", mae)
#
#             mse_scores.append(mse)
#             mae_scores.append(mae)
#             models.append(model)
#
#             logger.info(f"Validation on Current Season {current_season}, Week {week} - MSE: {mse}, MAE: {mae}")
#
#         # Average the scores across all validations
#         avg_mse = np.mean(mse_scores)
#         avg_mae = np.mean(mae_scores)
#
#         mlflow.log_metric("avg_MSE", avg_mse)
#         mlflow.log_metric("avg_MAE", avg_mae)
#
#         logger.info(f"Overall Average MSE: {avg_mse}")
#         logger.info(f"Overall Average MAE: {avg_mae}")
#
#         # Create an ensemble of the trained models
#         ensemble_model = EnsembleModel(models)
#         signature = infer_signature(X_preprocessed, ensemble_model.predict(X_preprocessed))
#         mlflow.sklearn.log_model(ensemble_model, "ensemble_model", signature=signature)
#         mlflow.sklearn.log_model(preprocessor, "preprocessor")
#         # Fit the final ensemble model on all data
#         ensemble_model.fit(X_preprocessed, y, sample_weight=sample_weights)
#
#     return ensemble_model, preprocessor


def create_preprocessor(cat_features, num_features):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features)
        ])

    return preprocessor


def exponential_decay(days, decay_rate=0.005):
    return np.exp(-decay_rate * days)


def train_model(df: pd.DataFrame, current_season: int, current_week: int, experiment_name: str,
                validation_weeks_for_week1: int = 3, max_historical_years: int = 3):
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=f"Season_{current_season}_Week_{current_week}"):
        models = []
        mse_scores = []
        mae_scores = []
        mlflow.log_param("current_season", current_season)
        mlflow.log_param("current_week", current_week)
        mlflow.log_param("max_historical_years", max_historical_years)

        # Sort data by season and week
        df = df.sort_values(by=['season', 'week'])

        # Limit historical data
        df = df[df['season'] >= current_season - max_historical_years]

        # Calculate days since the start of the dataset
        df['days_since_start'] = (df['season'] - df['season'].min()) * 365 + df['week'] * 7
        max_days = df['days_since_start'].max()

        # Apply exponential decay to create time-based weights
        df['time_weight'] = exponential_decay(max_days - df['days_since_start'])

        # Feature engineering for recency
        df['recent_performance'] = df.groupby('player_id')['fantasy_points'].transform(lambda x: x.ewm(span=5).mean())

        X = df[cat_features + numerical_features]
        y = df[model_prediction_vars]

        preprocessor = create_preprocessor(cat_features, numerical_features)
        X_preprocessed = preprocessor.fit_transform(X)

        # Create sample weights
        sample_weights = df['time_weight']

        for week in range(1, current_week + 1):
            if week == 1:
                train_mask = df['season'] < current_season
                val_mask = (df['season'] == current_season - 1) & (
                            df['week'] > df['week'].max() - validation_weeks_for_week1)
                logger.info(
                    f"Week 1: Training on {max_historical_years} years of data, validating on last {validation_weeks_for_week1} weeks of previous season")
            else:
                train_mask = (df['season'] < current_season) | ((df['season'] == current_season) & (df['week'] < week))
                val_mask = (df['season'] == current_season) & (df['week'] == week)

            train_X = X_preprocessed[train_mask]
            train_y = y[train_mask]
            train_weights = sample_weights[train_mask]

            val_X = X_preprocessed[val_mask]
            val_y = y[val_mask]

            if train_X.shape[0] == 0:
                logger.error(f"No training data for Season {current_season}, Week {week}")
                continue

            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(train_X, train_y, sample_weight=train_weights)

            if val_X.shape[0] > 0:
                y_pred = model.predict(val_X)
                mse = mean_squared_error(val_y, y_pred)
                mae = mean_absolute_error(val_y, y_pred)

                mse_scores.append(mse)
                mae_scores.append(mae)

                mlflow.log_metric(f"MSE_week_{week}", mse)
                mlflow.log_metric(f"MAE_week_{week}", mae)

                logger.info(f"Validation on Season {current_season}, Week {week} - MSE: {mse}, MAE: {mae}")
            else:
                logger.warning(f"No validation data for Season {current_season}, Week {week}")

            models.append(model)

        if not models:
            logger.error("No models were trained. Check your data and filtering conditions.")
            return None, preprocessor

        if mse_scores:
            avg_mse = np.mean(mse_scores)
            mlflow.log_metric("avg_MSE", avg_mse)
            logger.info(f"Overall Average MSE: {avg_mse}")

        if mae_scores:
            avg_mae = np.mean(mae_scores)
            mlflow.log_metric("avg_MAE", avg_mae)
            logger.info(f"Overall Average MAE: {avg_mae}")

        ensemble_model = EnsembleModel(models)
        ensemble_model.fit(X_preprocessed, y, sample_weight=sample_weights)

        signature = infer_signature(X_preprocessed, ensemble_model.predict(X_preprocessed))
        mlflow.sklearn.log_model(ensemble_model, "ensemble_model", signature=signature)
        mlflow.sklearn.log_model(preprocessor, "preprocessor")

        return ensemble_model, preprocessor


def save_model_and_preprocessor(ensemble_model, preprocessor, model_filename, preprocessor_filename):
    joblib.dump(ensemble_model, model_filename)
    joblib.dump(preprocessor, preprocessor_filename)

def main(season: int, week: int):
    logger.info(f'Running model training for season {season} and week {week}')

    df = read_weekly_stats()
    # _, _ = train_model_with_historical_iterations(df, season, week, "iterate-hist-seasons")
    ensemble_model, preprocessor = train_model(df, season, week, "iterate-only-curr-season")
    model_filename = settings.FF_PREDICTION_MODEL_FILE.format(season=season, week=week)
    preprocessor_filename = settings.FF_PREDICTION_PREPROCESSOR_FILE.format(season=season, week=week)
    save_model_and_preprocessor(ensemble_model, preprocessor, model_filename, preprocessor_filename)