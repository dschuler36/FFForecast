import os

import httpx

from jobs.shared.logging_config import logger
from jobs.shared.settings import settings


def get_current_season_week():
    api_base = settings.API_BASE
    endpoint = os.path.join(api_base, 'api/current-season-week')
    res = httpx.get(endpoint)
    if res.status_code == 200:
        data = res.json()
        return data['season'], data['week']
