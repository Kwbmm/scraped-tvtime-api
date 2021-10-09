FROM python:3.8-alpine
COPY src/ /app/src/
COPY requirements.txt /app/
COPY Makefile /app/
COPY config.json /app/

WORKDIR /app

RUN pip3 install -r requirements.txt
CMD export FLASK_APP=/app/src/main.py && python3 -m flask run --host=0.0.0.0
