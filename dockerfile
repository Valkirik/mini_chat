FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install -U pip && \
    pip install poetry daphne && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /app/
COPY ../.env ./.env
COPY entrypoint.sh /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "bash", "/app/entrypoint.sh"]