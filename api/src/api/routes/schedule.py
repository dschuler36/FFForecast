from fastapi import APIRouter, Depends

import deps
from api.services.schedule_service import ScheduleService

router = APIRouter(tags=['schedule'], prefix='/api')


@router.get('/current-season-week')
async def get_current_season_week(
        schedule_service: ScheduleService = Depends(deps.get_schedule_service)):
    return await schedule_service.get_current_season_week()
