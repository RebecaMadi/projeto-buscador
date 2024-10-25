FROM python:3.11-slim

WORKDIR /indexer

COPY . /indexer/

RUN pip install --upgrade pip \
    && pip install poetry==1.8.3
RUN poetry install