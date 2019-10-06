FROM python:3.7-slim

COPY Pipfile* /

RUN buildDeps=' \
	gcc \
	libc-dev \
    ' \
    && apt-get update && apt-get install -y --no-install-recommends $buildDeps libpq-dev \
    && pip install pipenv \
    && pipenv install --system --skip-lock  \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

COPY /core/ /core/
COPY /test/ /test/

WORKDIR /core

ENV PYTHONPATH=/
