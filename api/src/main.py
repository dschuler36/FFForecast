from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import predictions, schedule, accuracy
from api.settings import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.UI_URL],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(predictions.router)
app.include_router(schedule.router)
app.include_router(accuracy.router)
