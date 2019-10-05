FROM python:3.7-slim

COPY Pipfile* /

RUN buildDeps=' \
	gcc \
	libc-dev \
    ' \
    && apt-get update && apt-get install -y --no-install-recommends $buildDeps \
    && pip install pipenv \
    && pipenv install --system --deploy \
    && apt-get purge -y --auto-remove $buildDeps

RUN pipenv install --system --deploy

COPY /core /core/
COPY /test /test/

WORKDIR /core

ENV PYTHONPATH=/