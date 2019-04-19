FROM python:3.7.3-alpine
MAINTAINER Simon Sorensen (hello@simse.io)

RUN apk add --no-cache bash
COPY . /app/chronos

RUN apk add --update nodejs nodejs-npm yarn
WORKDIR /app/chronos/chronos-ui
RUN yarn install
RUN yarn build

EXPOSE 5000
VOLUME /chronos
ENV CHRONOS_PATH=/chronos
ENV CHRONOS=yes_sir_docker

WORKDIR /app/chronos
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt
ENTRYPOINT python chronos.py
