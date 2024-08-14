import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error

def read_weekly_stats() -> pd.DataFrame:
    return pd.read_sql(
        sql='select * from weekly_stats;',
        con='postgresql://ff:ff@0.0.0.0:5432/ff'
    )



def train_model(df):
    # Drop columns with all NaN values
    df = df.dropna(axis=1, how='all')

    # Alternatively, drop columns with all zeros (if zeros are problematic)
    df = df.loc[:, (df != 0).any(axis=0)]

    # Drop columns with only one unique value (no variance)
    df = df.loc[:, df.nunique() > 1]

    # Filter data for training and testing
    train_data = df[df['season'].isin([2020, 2021, 2022])]
    test_data = df[df['season'] == 2023]

    # todo: add home_away column
    categorical_features = ['player_id', 'recent_team','opponent_team']
    numerical_features = ['completions', 'attempts',  'sacks',
        'sack_yards', 'passing_air_yards', 'passing_yards_after_catch', 'passing_first_downs', 'passing_epa',
        'passing_2pt_conversions', 'pacr', 'dakota', 'carries',  'rushing_first_downs',
        'rushing_epa', 'targets',  'receiving_air_yards', 'receiving_yards_after_catch', 'receiving_epa',
         'racr', 'target_share', 'air_yards_share', 'wopr', 'special_teams_tds']
    target_variables = ['passing_yards', 'passing_tds', 'interceptions', 'fumbles', 'rushing_yards', 'rushing_tds',
                        'rushing_2pt_conversions', 'receptions', 'receiving_yards', 'receiving_tds',
                        'receiving_2pt_conversions']

    # Split into input features and target variables
    X_train = train_data[categorical_features + numerical_features]
    y_train = train_data[target_variables]

    X_test = test_data[categorical_features + numerical_features]
    y_test = test_data[target_variables]

    # One-hot encode categorical features
    X_train_encoded = pd.get_dummies(X_train, columns=categorical_features)
    X_test_encoded = pd.get_dummies(X_test, columns=categorical_features)

    # Ensure both train and test sets have the same feature columns
    X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='left', axis=1, fill_value=0)

    from sklearn.ensemble import RandomForestRegressor

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_encoded, y_train)

    # Make predictions on the 2023 season
    y_pred = model.predict(X_test_encoded)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Mean Squared Error on 2023 data: {mse}")
    print(f"Mean Absolute Error on 2023 data: {mae}")
    return model


def main(season: int, week: int):
    df = read_weekly_stats()
    model = train_model(df)
    model_filename = f'ff_pred_{season}_{week}.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(model, f)
