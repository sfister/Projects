# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
# https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
# scollier <scollier@redhat.com>
FROM centos:centos7
MAINTAINER The CentOS Project <cloud-ops@centos.org>

# Install utilities
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install epel-release

# Install languages
RUN yum -y install java
RUN yum -y install nodejs
RUN yum -y install npm
ADD logstash.repo /etc/yum.repos.d/logstash.repo


RUN yum -y install logstash
RUN cd /opt/logstash; bin/plugin install contrib; cd ~
RUN chkconfig logstash on

CMD ["/run.sh"]

EXPOSE 80
