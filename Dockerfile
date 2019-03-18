FROM python:3.7.2-alpine
LABEL maintainer=asinggih

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# install postgresql-client using alpine package manager
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# Remove the helper dependencies to install our reqs.
RUN apk del .tmp-build-deps

# create an app directory in '/''
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a user that only runs application.
RUN adduser -D user
USER user