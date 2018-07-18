FROM python:3.6-alpine

RUN apk add --update build-base nodejs yarn
RUN npm install --global webpack webpack-cli

RUN mkdir /install/

COPY src /install/hub
RUN pip install -e /install/hub
RUN cd /install/hub/home_automation_hub && yarn install && yarn run build:dev

COPY modules /install/modules
RUN pip install -e /install/modules/*

CMD ["home-automation-hub"]