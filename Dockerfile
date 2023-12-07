FROM python:3.8-slim-buster

ENV PYTHONDONTWRITTEBYTEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HTTPS_PROXY="http://fodev.org:8118"
RUN mkdir -p /app
WORKDIR /app
COPY ./core .

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt