import pandas as pd
import pickle

from scipy import sparse
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer


def read_weekly_stats() -> pd.DataFrame:
    return pd.read_sql(
        sql='select * from weekly_stats;',
        con='postgresql://ff:ff@0.0.0.0:5432/ff'
    )



def train_model(df: pd.DataFrame):
    # todo: add home_away column
    cat_features_to_encode = ['player_id', 'team', 'opponent']
    target_variables = ['passing_yards', 'passing_tds', 'interceptions', 'fumbles', 'rushing_yards', 'rushing_tds',
                        'rushing_2pt_conversions', 'receptions', 'receiving_yards', 'receiving_tds',
                        'receiving_2pt_conversions']

    # Filter data for training and testing
    df = df[cat_features_to_encode + target_variables + ['season']]
    train_data = df[df['season'].isin([2020, 2021, 2022])]
    test_data = df[df['season'] == 2023]


    # TODO: make this preprocessor into a shared location to be reused at prediction time
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat_features', OneHotEncoder(sparse_output=True, handle_unknown='ignore'), cat_features_to_encode)
        ],
        remainder='passthrough'
    )

    # Fit the preprocessor on the training data
    X_train = train_data.drop(columns=target_variables)
    X_train_encoded = preprocessor.fit_transform(X_train)

    # Transform the test data
    X_test = test_data.drop(columns=target_variables)
    X_test_encoded = preprocessor.transform(X_test)

    # Prepare target variables
    y_train = train_data[target_variables]
    y_test = test_data[target_variables]

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_encoded, y_train)

    # Make predictions on the 2023 season
    y_pred = model.predict(X_test_encoded)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Mean Squared Error on 2023 data: {mse}")
    print(f"Mean Absolute Error on 2023 data: {mae}")

    return model, preprocessor

# Function to get feature names (useful for interpretation)
def get_feature_names(column_transformer):
    feature_names = []
    for name, transformer, column in column_transformer.transformers_:
        if name != 'remainder':
            if hasattr(transformer, 'get_feature_names_out'):
                feature_names.extend(transformer.get_feature_names_out(column))
            else:
                feature_names.extend(column)
    return feature_names


def main(season: int, week: int):
    df = read_weekly_stats()
    model = train_model(df)
    model_filename = f'ff_pred_{season}_{week}.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    main(2023, 1)