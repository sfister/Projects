from debian:sid

run apt-get update 
run apt-get install -y \
   wget \
   curl 

RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee /etc/apt/sources.list.d/webupd8team-java.list
RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886
RUN apt-get update
RUN apt-get install -y libxrender1 libxtst6
RUN apt-get update \
    && apt-get install -y wget openssl ca-certificates \
    && cd /tmp \
    && wget -qO jdk8.tar.gz \
       --header "Cookie: oraclelicense=accept-securebackup-cookie" \
       http://download.oracle.com/otn-pub/java/jdk/8u40-b25/jdk-8u40-linux-x64.tar.gz \
    && tar xzf jdk8.tar.gz -C /opt \
    && mv /opt/jdk* /opt/java \
    && rm /tmp/jdk8.tar.gz \
    && update-alternatives --install /usr/bin/java java /opt/java/bin/java 100 \
    && update-alternatives --install /usr/bin/javac javac /opt/java/bin/javac 100

ENV JAVA_HOME /opt/java

RUN wget http://protege.stanford.edu/download/protege/3.5/installanywhere/Web_Installers/InstData/Linux_64bit/NoVM/install_protege_3.5.bin
RUN sh install_protege_3.5.bin -i console

RUN wget http://www.enterprise-architecture.org/downloads_area/essentialinstall4_3_1.jar

ENV TOMCAT_MAJOR_VERSION 7
ENV TOMCAT_MINOR_VERSION 7.0.55
ENV CATALINA_HOME /tomcat

# INSTALL TOMCAT
RUN wget -q https://archive.apache.org/dist/tomcat/tomcat-${TOMCAT_MAJOR_VERSION}/v${TOMCAT_MINOR_VERSION}/bin/apache-tomcat-${TOMCAT_MINOR_VERSION}.tar.gz && \
    wget -qO- https://archive.apache.org/dist/tomcat/tomcat-${TOMCAT_MAJOR_VERSION}/v${TOMCAT_MINOR_VERSION}/bin/apache-tomcat-${TOMCAT_MINOR_VERSION}.tar.gz.md5 | md5sum -c - && \
    tar zxf apache-tomcat-*.tar.gz && \
    rm apache-tomcat-*.tar.gz && \
    mv apache-tomcat* tomcat

#ADD create_tomcat_admin_user.sh /create_tomcat_admin_user.sh
ADD run.sh /run.sh
RUN chmod +x /*.sh

RUN wget http://www.graphviz.org/pub/graphviz/stable/ubuntu/ub10.10/x86_64/graphviz_2.26.3-1_amd64.deb

RUN dpkg -f graphviz_2.26.3-1_amd64.deb


