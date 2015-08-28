from centos:7

RUN yum install -y epel-release
RUN yum -y update
RUN yum install -y git python-pip MySQL-python python-devel numpy gcc-c++ zeromq
RUN pip install crate elasticsearch ipython[all]
RUN mkdir github && cd github && git init 
ADD ipython_notebook_config.py ~/.ipython/profile_default/ipython_notebook_config.py
RUN mkdir -p /consul-data && yum install -y wget curl unzip  && mkdir -p /consul && pip install python-consul &&\
wget https://dl.bintray.com/mitchellh/consul/0.5.2_linux_amd64.zip -O consul.zip && unzip -j consul.zip consul -d /usr/bin
RUN wget -O ui.zip http://dl.bintray.com/mitchellh/consul/0.5.2_web_ui.zip \
  && unzip ui.zip \
  && mv dist /consul-ui 

RUN pip install cassandra-driver
RUN pip install rethinkdb

ADD startipython /startipython

