FROM python:3.9.13

RUN mkdir /numbersff-api
WORKDIR /numbersff-api

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src

ENV POSTGRES_CONN_STRING=postgresql+asyncpg://postgres:ff@database:5432/ff

WORKDIR ./src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]