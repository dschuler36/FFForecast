from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import predictions
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(predictions.router)
