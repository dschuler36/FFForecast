from fastapi import APIRouter, Depends

import deps
from api.services.accuracy_service import AccuracyService

router = APIRouter(tags=['schedule'], prefix='/api')


@router.get('/accuracy/diffs')
async def get_prediction_diffs(
        season: int,
        week: int,
        actuals_service: AccuracyService = Depends(deps.get_actuals_service)):
    return await actuals_service.get_prediction_diffs(season, week)


@router.get('/accuracy/metrics')
async def get_accuracy_metrics(
        season: int,
        week: int,
        actuals_service: AccuracyService = Depends(deps.get_actuals_service)):
    return await actuals_service.get_accuracy_metrics(season, week)
