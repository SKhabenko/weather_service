FROM python:3.7-alpine3.9

ENV TZ 'Europe/Moscow'

COPY ./requirements /requirements
COPY ./docker/docker-entrypoint.sh /

RUN mkdir -p /opt/weather_service/
WORKDIR /opt/weather_service

RUN apk update \
    && cat /requirements/apk.txt | xargs apk add  --no-cache \
    && pip install --upgrade pip \
    && pip install -r /requirements/python.txt \
    && echo $TZ >  /etc/timezone

ENTRYPOINT ["/docker-entrypoint.sh"]
