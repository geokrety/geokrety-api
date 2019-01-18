FROM alpine:latest

MAINTAINER Mathieu Alorent <contact@geokretymap.org>

# Add extension to php
RUN apk add --no-cache \
        python3 \
        py-pip \
        py-mysqldb \
        vim \
        git \
        mariadb-dev \
        gcc \
        python2-dev \
 	      musl-dev \
        libffi-dev

COPY requirements.txt requirements.txt
COPY requirements requirements
RUN  pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

WORKDIR /src
EXPOSE 5000

CMD gunicorn -w 4 -b 0.0.0.0:5000 --reload app.main:app --access-logfile=- --error-logfile=-
