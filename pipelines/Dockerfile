FROM python:3.9-slim

WORKDIR /app

# directory for storing model artifacts
RUN mkdir artifacts

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
# COPY ./.env.local .

ENV PIPELINE_TO_RUN=run_ml_pipeline.py
ENV SEASON=2023
ENV WEEK=1
# commenting out so it doesn't always run locally when testing api
CMD python ${PIPELINE_TO_RUN} ${SEASON} ${WEEK}
