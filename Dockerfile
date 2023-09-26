#FROM python:3.7.7-stretch AS BASE
FROM python:3.8 AS BASE

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        git \
        jq \
        libgomp1 \
        vim

WORKDIR /app

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip

RUN pip install rasa
RUN pip install django

ADD config.yml config.yml
ADD domain.yml domain.yml
ADD credentials.yml credentials.yml
ADD endpoints.yml endpoints.yml
ADD manage.py manage.py
ADD data data
ADD actions actions
ADD rasaweb rasaweb
ADD rasadjango rasadjango
ADD templates templates
ADD static static
