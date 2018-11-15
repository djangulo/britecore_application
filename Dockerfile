FROM python:3.6-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apk update \
    && apk add --virtual .build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --deploy --skip-lock --system --dev

# clear build deps
RUN apk del .build-deps

COPY . /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
