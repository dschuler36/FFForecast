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


from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerStats(Base):
    __tablename__ = 'weekly_stats'

    fantasy_points_ppr = Column(Float)
    racr = Column(Float)
    target_share = Column(Float)
    air_yards_share = Column(Float)
    wopr = Column(Float)
    special_teams_tds = Column(Float)
    depth_ranking = Column(Integer)
    fantasy_points = Column(Float)
    season = Column(Integer, primary_key=True)
    week = Column(Integer, primary_key=True)
    age = Column(Float)
    completions = Column(Integer)
    attempts = Column(Integer)
    passing_yards = Column(Float)
    passing_tds = Column(Integer)
    interceptions = Column(Float)
    fumbles = Column(Float)
    sacks = Column(Float)
    sack_yards = Column(Float)
    passing_air_yards = Column(Float)
    passing_yards_after_catch = Column(Float)
    passing_first_downs = Column(Float)
    passing_epa = Column(Float)
    passing_2pt_conversions = Column(Integer)
    pacr = Column(Float)
    dakota = Column(Float)
    carries = Column(Integer)
    rushing_yards = Column(Float)
    rushing_tds = Column(Integer)
    rushing_first_downs = Column(Float)
    rushing_epa = Column(Float)
    rushing_2pt_conversions = Column(Integer)
    receptions = Column(Integer)
    targets = Column(Integer)
    receiving_yards = Column(Float)
    receiving_tds = Column(Integer)
    receiving_air_yards = Column(Float)
    receiving_yards_after_catch = Column(Float)
    receiving_first_downs = Column(Float)
    receiving_epa = Column(Float)
    receiving_2pt_conversions = Column(Integer)
    player_display_name = Column(String)
    position = Column(String)
    headshot_url = Column(String)
    team = Column(String)
    home_away = Column(String)
    player_id = Column(String, primary_key=True)
    opponent = Column(String)
