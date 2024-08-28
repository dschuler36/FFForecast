from fastapi import APIRouter, Depends

import deps
from api.services.actuals_service import ActualsService
from api.services.schedule_service import ScheduleService

router = APIRouter(tags=['schedule'], prefix='/api')


@router.get('/get-prediction-accuracy')
async def get_prediction_accuracy(
        season: int,
        week: int,
        actuals_service: ActualsService = Depends(deps.get_actuals_service)):
    return await actuals_service.get_prediction_accuracy(season, week)
