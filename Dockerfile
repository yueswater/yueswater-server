FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=2.0.1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    wget \
    ca-certificates \
    texlive-xetex \
    texlive-lang-chinese \
    texlive-plain-generic \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-science \
    lmodern \
    fontconfig \
    && ARCH=$(dpkg --print-architecture) \
    && wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-${ARCH}.deb \
    && dpkg -i pandoc-3.1.11-1-${ARCH}.deb \
    && rm pandoc-3.1.11-1-${ARCH}.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

RUN mkdir -p /usr/share/fonts/truetype/custom \
    && cp static/fonts/*.ttf /usr/share/fonts/truetype/custom/ \
    && fc-cache -f -v \
    && mkdir -p /app/fonts \
    && cp static/fonts/*.ttf /app/fonts/

RUN mkdir -p /app/staticfiles

EXPOSE 8000 

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python -m gunicorn --bind 0.0.0.0:${PORT:-8088} --workers 2 --worker-class sync --timeout 120 --log-level debug config.wsgi:application"]