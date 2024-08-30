from sqlalchemy import Column, BigInteger, Float, String, Integer, Date, Time
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WeeklyPredictionBase(Base):
    __tablename__ = 'weekly_predictions_base'

    week = Column(BigInteger, primary_key=True, nullable=False)
    season = Column(BigInteger, primary_key=True, nullable=False)
    player_id = Column(String, primary_key=True, nullable=False)

    passing_yards = Column(Float)
    passing_tds = Column(Float)
    interceptions = Column(Float)
    fumbles = Column(Float)
    rushing_yards = Column(Float)
    rushing_tds = Column(Float)
    rushing_2pt_conversions = Column(Float)
    receptions = Column(Float)
    receiving_yards = Column(Float)
    receiving_tds = Column(Float)
    receiving_2pt_conversions = Column(Float)
    passing_2pt_conversions = Column(Float)
    opponent = Column(String)
    player_name = Column(String)
    team = Column(String)
    position = Column(String)


class WeeklyPredictionStdHalfPPR(Base):
    __tablename__ = 'weekly_predictions_std_half_ppr'

    season = Column(BigInteger, primary_key=True, nullable=False)
    week = Column(BigInteger, primary_key=True, nullable=False)
    player_id = Column(String, primary_key=True, nullable=False)

    fantasy_points = Column(Float)


class WeeklyPredictionStdFullPPR(Base):
    __tablename__ = 'weekly_predictions_std_full_ppr'

    season = Column(BigInteger, primary_key=True, nullable=False)
    week = Column(BigInteger, primary_key=True, nullable=False)
    player_id = Column(String, primary_key=True, nullable=False)

    fantasy_points = Column(Float)


class Schedule(Base):
    __tablename__ = 'schedule'

    game_id = Column(String, primary_key=True)
    season = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    gameday = Column(Date, nullable=False)
    gametime = Column(Time, nullable=False)
    weekdate = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)

class PredictionDiff(Base):
    __tablename__ = 'prediction_diffs'

    player_id = Column(String(255), primary_key=True)
    season = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)
    player_name = Column(String)
    team = Column(String)
    opponent = Column(String)
    position = Column(String)
    fantasy_points = Column(Float)
    passing_yards = Column(Float)
    passing_tds = Column(Float)
    interceptions = Column(Float)
    fumbles = Column(Float)
    rushing_yards = Column(Float)
    rushing_tds = Column(Float)
    rushing_2pt_conversions = Column(Float)
    receptions = Column(Float)
    receiving_yards = Column(Float)
    receiving_tds = Column(Float)
    receiving_2pt_conversions = Column(Float)
    passing_2pt_conversions = Column(Float)
    fantasy_points_actual = Column(Float)
    passing_yards_actual = Column(Float)
    passing_tds_actual = Column(Integer)
    interceptions_actual = Column(Float)
    fumbles_actual = Column(Float)
    rushing_yards_actual = Column(Float)
    rushing_tds_actual = Column(Integer)
    rushing_2pt_conversions_actual = Column(Integer)
    receptions_actual = Column(Integer)
    receiving_yards_actual = Column(Float)
    receiving_tds_actual = Column(Integer)
    receiving_2pt_conversions_actual = Column(Integer)
    passing_2pt_conversions_actual = Column(Integer)
    fantasy_points_diff = Column(Float)
    passing_yards_diff = Column(Float)
    passing_tds_diff = Column(Float)
    interceptions_diff = Column(Float)
    fumbles_diff = Column(Float)
    rushing_yards_diff = Column(Float)
    rushing_tds_diff = Column(Float)
    rushing_2pt_conversions_diff = Column(Float)
    receptions_diff = Column(Float)
    receiving_yards_diff = Column(Float)
    receiving_tds_diff = Column(Float)
    receiving_2pt_conversions_diff = Column(Float)
    passing_2pt_conversions_diff = Column(Float)

class AccuracyMetric(Base):
    __tablename__ = 'accuracy_metrics'

    season = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)
    MAE = Column(Float)
    MSE = Column(Float)
    RMSE = Column(Float)
    R_squared = Column(Float)