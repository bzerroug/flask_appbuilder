FROM debian:jessie

# Install system dependencies:
# - pip
# - dependencies for psycopg2: python-dev libpq-dev
# - dependencies for scipy: gfortran libopenblas-dev liblapack-dev
RUN apt-get update && apt-get install -y \
    python-pip \
    python-dev libpq-dev \
    gfortran libopenblas-dev liblapack-dev

# Install application
# Required to have numpy installed beore running pip install .
RUN pip install numpy

# Pandas is long to install, cache build with docker.
RUN pip install pandas

# Speed up build, and cache psycopg2 and sqlalchemy install
RUN pip install psycopg2
RUN pip install sqlalchemy

# Put application in /app
ADD . /app
WORKDIR /app

# Install app
RUN pip install -e .
