FROM python:3.7-alpine

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/backend

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/backend/Pipfile
RUN pipenv install --skip-lock --system --dev

# clear build deps
RUN apk del .build-deps


COPY . /usr/src/backend/