from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import WeeklyPredictionBase, WeeklyPredictionStdHalfPPR, WeeklyPredictionStdFullPPR


class PredictionsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def get_base_predictions_query(season: int, week: int, league_config_predictions):
        stmt = (
            select(WeeklyPredictionBase, league_config_predictions.fantasy_points)
            .join(league_config_predictions, WeeklyPredictionBase.player_id == league_config_predictions.player_id)
            .where(
                WeeklyPredictionBase.season == season,
                WeeklyPredictionBase.week == week
            )
            .order_by(league_config_predictions.fantasy_points.desc())
            .limit(150)
        )
        return stmt

    async def get_half_ppr_predictions(self, season: int, week: int):
        stmt = self.get_base_predictions_query(season, week, WeeklyPredictionStdHalfPPR)
        result = await self.db.execute(stmt)
        predictions = result.fetchall()  # This returns a list of tuples (WeeklyPredictionBase, WeeklyPredictionStdHalfPPR)
        # Unpack tuples into a list of dicts or any other structure you need
        unpacked_predictions = [
            {"base": base, "fantasy_points": std_half_ppr}
            for base, std_half_ppr in predictions
        ]
        return unpacked_predictions

    async def get_full_ppr_predictions(self, season: int, week: int):
        stmt = self.get_base_predictions_query(season, week, WeeklyPredictionStdFullPPR)
        result = await self.db.execute(stmt)
        predictions = result.fetchall()  # This returns a list of tuples (WeeklyPredictionBase, WeeklyPredictionStdHalfPPR)
        # Unpack tuples into a list of dicts or any other structure you need
        unpacked_predictions = [
            {"base": base, "fantasy_points": std_full_ppr}
            for base, std_full_ppr in predictions
        ]
        return unpacked_predictions