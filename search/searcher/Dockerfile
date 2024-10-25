FROM python:3.11-slim

WORKDIR /searcher

RUN pip install --upgrade pip \
    && pip install poetry==1.8.3

RUN pip config set global.timeout 6000

COPY pyproject.toml poetry.lock* /searcher/

RUN poetry install

COPY . /searcher/

EXPOSE 3003

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3003"]