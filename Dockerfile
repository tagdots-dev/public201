FROM python:3.9.7-slim-buster

WORKDIR /app
COPY . /app

RUN apt-get update && \
    pip install --no-cache-dir -r /app/requirements.txt  && \
    pip install --no-cache-dir -e . && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
