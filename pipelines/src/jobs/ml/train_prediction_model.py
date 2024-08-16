import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder

from shared.settings import settings


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
    # Data preprocessing steps
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, (df != 0).any(axis=0)]
    df = df.loc[:, df.nunique() > 1]

    train_data = df[df['season'].isin([2020, 2021, 2022])]
    test_data = df[df['season'] == 2023]

    cat_features_to_encode = ['player_id', 'team', 'opponent']
    target_variables = ['passing_yards', 'passing_tds', 'interceptions', 'fumbles', 'rushing_yards', 'rushing_tds',
                        'rushing_2pt_conversions', 'receptions', 'receiving_yards', 'receiving_tds',
                        'receiving_2pt_conversions', 'passing_2pt_conversions']

    # Create and fit the preprocessor
    preprocessor = create_preprocessor(cat_features_to_encode)

    # Prepare the data
    X_train = train_data[cat_features_to_encode]
    y_train = train_data[target_variables]
    X_test = test_data[cat_features_to_encode]
    y_test = test_data[target_variables]

    # Fit the preprocessor and transform the data
    X_train_preprocessed = preprocessor.fit_transform(X_train)

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_preprocessed, y_train)

    # Transform test data and make predictions
    X_test_preprocessed = preprocessor.transform(X_test)
    y_pred = model.predict(X_test_preprocessed)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Mean Squared Error on 2023 data: {mse}")
    print(f"Mean Absolute Error on 2023 data: {mae}")

    return model, preprocessor


# Save model and preprocessor
def save_model_and_preprocessor(model, preprocessor, model_filename, preprocessor_filename):
    joblib.dump(model, model_filename)
    joblib.dump(preprocessor, preprocessor_filename)


def main(season: int, week: int):
    df = read_weekly_stats()
    model, preprocessor = train_model(df)
    model_filename = settings.FF_PREDICTION_MODEL_FILE.format(season=season, week=week)
    preprocessor_filename = settings.FF_PREDICTION_PREPROCESSOR_FILE.format(season=season, week=week)
    save_model_and_preprocessor(model, preprocessor, model_filename, preprocessor_filename)
