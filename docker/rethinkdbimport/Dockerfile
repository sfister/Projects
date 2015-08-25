FROM rethinkdb

MAINTAINER Steven Fister


RUN apt-get update \
	&& apt-get install -y python wget curl
RUN apt-get install -y \
	python-pip

RUN pip install rethinkdb

VOLUME ["/data"]

WORKDIR /data


