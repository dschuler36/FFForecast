from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_date

from api.models import Schedule


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_season_week(self):
        # TODO: can make this testable by passing in current_date instead of pulling it here
        stmt = (
            select(Schedule.season, Schedule.week)
            .where(current_date() <= Schedule.gameday)
            .order_by(Schedule.gameday)
            .limit(1)
        )

        result = await self.db.execute(stmt)
        row = result.fetchone()

        if row:
            return {"season": row.season, "week": row.week}
        else:
            return None
