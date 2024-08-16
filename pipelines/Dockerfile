FROM python:3.9-slim

WORKDIR /app

COPY pipelines/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY pipelines/src/ .
COPY shared ./shared
COPY .env.local .

ENV PIPELINE_TO_RUN=run_ml_pipeline.py

# Use the environment variable in the CMD
# CMD python ${PIPELINE_TO_RUN}
