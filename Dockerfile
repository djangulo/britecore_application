FROM python:3.6-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apk update \
    && apk add --virtual build-deps gcc musl-dev \
    && apk add postgresql-dev python3-dev 

RUN pip install --upgrade pip \
    && pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --deploy --skip-lock --system --dev \
    && apk del build-deps
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app/
ENTRYPOINT ["/bin/sh", "/usr/src/app/entrypoint.sh"]
