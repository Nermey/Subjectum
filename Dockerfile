FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

CMD gunicorn auth:app --bind=0.0.0.0:6100


