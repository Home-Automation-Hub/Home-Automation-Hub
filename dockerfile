FROM python:3.6-alpine

RUN apk add --update build-base nodejs yarn npm
RUN npm install --global webpack webpack-cli

RUN mkdir /install/

# Copy in just setup.py and install, this will install all of the
# Python dependencies ONLY if setup.py has been changed, not just if ANY
# file has been changed
COPY src/setup.py /install/hub/setup.py
RUN mkdir /install/hub/home_automation_hub
RUN pip install -e /install/hub

# Copy just package.json in for now and install dependencies, this means
# that dependencies will be reinstalled ONLY if package.json is changed
COPY src/home_automation_hub/package.json /install/hub/home_automation_hub/package.json
RUN cd /install/hub/home_automation_hub && yarn install

# Now copy in the frontend source code and build it, this means that
# we will rebuild the frontend ONLY if a piece of frontend source code
# is modified
COPY src/home_automation_hub/frontend_src /install/hub/home_automation_hub/frontend_src
COPY src/home_automation_hub/webpack.conf.js /install/hub/home_automation_hub/webpack.conf.js
RUN cd /install/hub/home_automation_hub && yarn run build:dev

# Remove node_modules as this is no longer required now that we have
# built the frontend and leaving it in places causes issues with pip
RUN rm -rf /install/hub/home_automation_hub/node_modules

# Now copy in the rest of the system and run pip install again, this
# will not reinstall all Python dependencies as they have been don
# above
COPY src /install/hub
RUN pip install /install/hub

COPY modules /install/modules
RUN pip install /install/modules/*

# PYTHONUNBUFFERED ensures that log lines from the application are
# output immediately when using docker logs or docker attach rather than
# being "batched" and displayed very infrequently
ENV PYTHONUNBUFFERED=0
CMD ["home-automation-hub"]