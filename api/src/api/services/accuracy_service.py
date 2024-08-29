from sqlalchemy import select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PredictionDiff, AccuracyMetric
from api.services.predictions_service import PredictionsService


class AccuracyService:
    def __init__(self, db: AsyncSession, predictions_service: PredictionsService):
        self.db = db
        self.predictions_service = predictions_service

    async def get_prediction_diffs(self, season: int, week: int):
        stmt = (
            select(PredictionDiff)
            .where(PredictionDiff.season == season, PredictionDiff.week == week)
        )
        preds = (await self.db.execute(stmt)).scalars().all()
        return preds


    async def get_accuracy_metrics(self, season: int, week: int):
        stmt = (
            select(AccuracyMetric)
            .where(AccuracyMetric.season == season, AccuracyMetric.week == week)
        )
        accuracy = (await self.db.execute(stmt)).scalar_one_or_none()
        return accuracy


    async def get_completed_season_weeks(self):
        stmt = (
            select(PredictionDiff.season, PredictionDiff.week).distinct()
        )
        results = await self.db.execute(stmt)

        unpacked_results = [
            {"season": row.season, "week": row.week}
            for row in results
        ]
        return unpacked_results
