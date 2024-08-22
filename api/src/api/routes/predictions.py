from fastapi import APIRouter, Depends

import deps
from api.services.predictions_service import PredictionsService
router = APIRouter(tags=['predictions'], prefix='/api')


@router.get('/predictions/half_ppr')
async def get_half_ppr_predictions(
        season: int,
        week: int,
        predictions_service: PredictionsService = Depends(deps.get_predictions_service)):
    return await predictions_service.get_half_ppr_predictions(season, week)


@router.get('/predictions/full_ppr')
async def get_full_ppr_predictions(
        season: int,
        week: int,
        predictions_service: PredictionsService = Depends(deps.get_predictions_service)):
    return await predictions_service.get_full_ppr_predictions(season, week)
