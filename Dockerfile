FROM python:3.7.2-alpine
LABEL maintainer=asinggih

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create an app directory in '/''
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a user that only runs application.
RUN adduser -D user
USER user