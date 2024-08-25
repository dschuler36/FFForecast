from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import get_db_session
from api.services.predictions_service import PredictionsService
from api.services.schedule_service import ScheduleService
from api.settings import Settings


def get_settings() -> Settings:
    return Settings()


def get_predictions_service(db: AsyncSession = Depends(get_db_session)) -> PredictionsService:
    return PredictionsService(db)


def get_schedule_service(db: AsyncSession = Depends(get_db_session)) -> ScheduleService:
    return ScheduleService(db)
