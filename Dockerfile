# app/Dockerfile

# pull the official docker image
FROM python:3.10-alpine

# set lables about app
LABEL maintainer="s.zhukovskii@ispsystem.com"
LABEL ru.isptech.akvolabean.moodlehack.version=v0.1.0

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on


COPY ./moodlehack /app
WORKDIR /app

COPY requirements.txt ./
COPY entrypoint.sh ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt


ENTRYPOINT [ "sh", "entrypoint.sh" ]
