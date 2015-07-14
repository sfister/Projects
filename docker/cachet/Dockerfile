# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
# https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
# scollier <scollier@redhat.com>
FROM centos:centos7
MAINTAINER Metocean Solutions(Steve Fister)

#Install utilities
RUN yum -y install wget curl epel-release python-pip sqlite git
RUN mkdir -p /var/www && cd /var/www && git clone https://github.com/cachethq/Cachet.git 

ADD nginx.repo /etc/yum.repo.d/.
RUN yum install -y nginx



