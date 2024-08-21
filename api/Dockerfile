FROM python:3.9.13

RUN mkdir /numbersff-api
WORKDIR /numbersff-api

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./start-app.sh ./src

ENV POSTGRES_CONN_STRING=postgresql+asyncpg://postgres:ff@database:5432/ff
ENV PORT=8000
WORKDIR ./src

CMD ["./start-app.sh"]