FROM python:3.11-slim

WORKDIR /fastapi-dag-service

COPY app/ /fastapi-dag-service/app/
COPY requirements.txt /fastapi-dag-service/

RUN pip install -r requirements.txt

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080