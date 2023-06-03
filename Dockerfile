FROM python:3.10.11

RUN python3 -m pip install --upgrade pip
RUN pip install poetry

RUN useradd -ms /bin/bash widgets

COPY --chown=widgets . /app/
WORKDIR /app/365widgets
RUN poetry install --no-dev

USER widgets