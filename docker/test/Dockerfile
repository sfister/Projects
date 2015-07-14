# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
# https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
# scollier <scollier@redhat.com>
FROM metocean/ops-base:1.0
MAINTAINER Metocean Solutions(Steve Fister)

#Install utilities
RUN yum -y install wget
RUN yum -y install curl
RUN yum -y install epel-release
RUN yum -y install python-pip
RUN pip install python-consul
RUN yum -y install MySQL-python
RUN pip install crate crash





