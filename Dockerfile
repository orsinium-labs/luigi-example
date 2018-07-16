FROM python:3.6-jessie

# get all packages from repos
RUN apt-get update -yq \
    && apt-get install -yq git

# install requirements
COPY ./project/Pipfile      /opt/project/Pipfile
COPY ./project/Pipfile.lock /opt/project/Pipfile.lock

# https://github.com/pypa/pipenv/blob/master/Dockerfile
RUN cd /opt/project/ \
    && set -ex \
    && pip install -U pip pipenv \
    && pipenv sync --python $(which python) --dev

WORKDIR /opt/project/
CMD ["pipenv sync && pipenv run ipython"]
