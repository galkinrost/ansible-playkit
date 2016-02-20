FROM ubuntu:14.04
MAINTAINER Oleg Poyaganov <oleg@poyaganov.com>

RUN apt-get -y update && \
    apt-get install -y software-properties-common && \
    apt-add-repository -y ppa:ansible/ansible && \
    apt-get -y update && \
    apt-get install -y ansible git openssl

VOLUME /opt
WORKDIR /opt
