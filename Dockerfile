FROM python:3.12-slim

ENV PYTHONUNBUFFERED = 1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && \
  apt-get install -y \
  zip \
  curl \
  wget \
  gnupg \
  gcc \
  && pip install --upgrade pip \
  && pip install poetry \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN poetry install --only main --no-cache && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


