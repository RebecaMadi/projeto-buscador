FROM python:3.11-slim

WORKDIR /coletasAPI

RUN pip install --upgrade pip \
    && pip install poetry==1.8.3

RUN pip config set global.timeout 6000

COPY pyproject.toml poetry.lock* /coletasAPI/

RUN poetry install

COPY . /coletasAPI/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "coletasapi.main:app", "--host", "0.0.0.0", "--port", "8000"]