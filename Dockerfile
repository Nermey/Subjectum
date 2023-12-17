FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY .env .

RUN export $(cat .env | xargs)

RUN pip install -r requirements.txt

COPY src .

CMD uvicorn auth:app --host $AUTH_HOST --port $AUTH_PORT
