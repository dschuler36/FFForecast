from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import WeeklyPredictionBase, WeeklyPredictionStdHalfPPR, WeeklyPredictionStdFullPPR


class PredictionsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def get_base_predictions_query(season: int, week: int, league_config_predictions):
        stmt = (
            select(WeeklyPredictionBase, WeeklyPredictionStdHalfPPR)
            .join(WeeklyPredictionStdHalfPPR, WeeklyPredictionBase.player_id == league_config_predictions.player_id)
            .where(
                WeeklyPredictionBase.season == season,
                WeeklyPredictionBase.week == week
            )
        )
        return stmt

    async def get_half_ppr_predictions(self, season: int, week: int):
        stmt = self.get_base_predictions_query(season, week, WeeklyPredictionStdHalfPPR)
        result = await self.db.execute(stmt)
        predictions = result.fetchall()
        return predictions

    async def get_full_ppr_predictions(self, season: int, week: int):
        stmt = self.get_base_predictions_query(season, week, WeeklyPredictionStdFullPPR)
        result = await self.db.execute(stmt)
        predictions = result.fetchall()
        return predictions