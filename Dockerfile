# get Python 3.10 without shell
# FROM python:3.10-alpine

# get Python 3.10 with shell
# FROM python:3.10-slim
FROM python:3.10-slim

ENV PYTHONUNBUFFERED  1 \
    PYTHONDONTWRITEBYTECODE 1 

WORKDIR /app

RUN pip install poetry \
    && touch README.md

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

RUN chmod a+x start_render.sh

CMD poetry run python manage.py migrate \
    && poetry run python manage.py runserver 0.0.0.0:8000