# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
# https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
# scollier <scollier@redhat.com>
FROM centos:centos7
MAINTAINER Metocean Solutions(Steve Fister)

#Install utilities
RUN yum -y install wget && yum -y install curl &&  yum -y install epel-release &&  yum -y install python-pip && pip install python-consul && pip install crate

#Add Consul
RUN mkdir -p /consul-data && consul/consul /usr/bin/consul

# Install crate
RUN bash -c "$(curl -L install.crate.io)" 

# Mount host volume for this node.
VOLUME ["/datastore"]

ADD crate.yml /etc/crate/crate.yml && mkdir -p /var/lock/subsys && touch /var/lock/subsys/crate
ADD run.sh /run.sh && chmod +x /run.sh

# Start Crate
CMD ["/run.sh"]

