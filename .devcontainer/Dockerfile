FROM python:3
ENV PYTHONUNBUFFERED 1 
RUN apt-get update && apt-get install -y git \
    && apk add --update-cache --no-cache \
    && pip install django \
    && apt-get install –y vim \