FROM python:3.6-alpine

RUN apk add --update build-base

RUN mkdir /install/

COPY src /install/hub
RUN pip install -e /install/hub

COPY modules /install/modules
RUN pip install -e /install/modules/*

CMD ["home-automation-hub"]