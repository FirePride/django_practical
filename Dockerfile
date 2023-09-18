FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /practical_app

RUN pip install --upgrade pip "poetry==1.6.1"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .
