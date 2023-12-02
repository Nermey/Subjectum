FROM python:3.10

RUN mkdir /authorization service

WORKDIR . /authorization service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

CMD ["gunicorn", "auth:app"]


