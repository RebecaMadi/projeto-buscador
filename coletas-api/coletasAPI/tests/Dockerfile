FROM python:3.11-slim

WORKDIR /tests

COPY . /tests/

RUN pip install pytest httpx pytest-asyncio

ENTRYPOINT ["wait-for-it", "coletasapi:8000", "--", "pytest", "./"]
