FROM python:3.9-slim as buil-step

RUN mkdir -p /app

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000

ENV FLASK_APP=./app.py
#RUN flask run -h 0.0.0.0
