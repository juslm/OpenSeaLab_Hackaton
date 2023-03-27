FROM python:3.9-alpine as buil-step

RUN mkdir -p /app

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN apk add --update alpine-sdk
RUN apk add --update-cache gdal 
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000

ENV FLASK_APP=./app.py
#RUN flask run -h 0.0.0.0
