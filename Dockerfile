FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=2.0.1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

RUN mkdir -p /app/staticfiles

EXPOSE 8000 

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python -m gunicorn --bind 0.0.0.0:${PORT:-8088} --workers 2 --worker-class sync --timeout 120 --log-level debug config.wsgi:application"]