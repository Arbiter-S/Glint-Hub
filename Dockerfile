FROM python:3.11.5-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV TZ="Asia/Tehran"
