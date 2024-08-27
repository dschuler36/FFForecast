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
ENV SEASON=""
ENV WEEK=""

CMD if [ -z "$SEASON" ] || [ -z "$WEEK" ]; then \
      python ${PIPELINE_TO_RUN}; \
    else \
      python ${PIPELINE_TO_RUN} True ${SEASON} ${WEEK}; \
    fi