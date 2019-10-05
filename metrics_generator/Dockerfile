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
# do not forget to put your keys here
COPY /keys /keys

WORKDIR /core

ENV PYTHONPATH=/