# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.11-alpine AS builder
EXPOSE 8000
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./backend ./backend
WORKDIR /app/backend
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]