FROM postgres:9.5.9

ENV TZ=Europe/Moscow

COPY ./docker/init.sql /docker-entrypoint-initdb.d/10-init.sql
