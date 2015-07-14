# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
# https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
# scollier <scollier@redhat.com>
FROM centos:centos7
MAINTAINER Metocean Solutions(Steve Fister)

#Install utilities
RUN yum -y install wget && yum -y install curl && yum -y install epel-release && yum -y install python-pip && pip install python-consul && yum -y install MySQL-python && mkdir -p /consul-data

#Add Consul
ADD consul/consul /usr/bin/consul

ADD run.sh /run.sh 
RUN chmod +x /run.sh

# Start Crate
CMD ["/run.sh"]

