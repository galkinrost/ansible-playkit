FROM ubuntu:18.04
MAINTAINER Rostislav Galkin <galkinrost@gmail.com>

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt-get install -y libssl-dev libffi-dev python-dev python-yaml python-jinja2 python-httplib2 python-keyczar python-paramiko python-setuptools python-pkg-resources git python-pip python-sphinx && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ADD . /opt/src

RUN cd /opt/src && \
    pip install packaging setuptools boto3 --upgrade && \
    python setup.py install && \
    rm -rf /opt/src && \
    cd / && \
    mkdir /etc/ansible/ && \
    echo '[local]\nlocalhost\n' > /etc/ansible/hosts && \
    mkdir /opt/ansible/ && \
    git clone --branch stable-2.7 --depth 1 https://github.com/ansible/ansible.git /opt/ansible/ansible

RUN cd /opt/ansible/ansible && \
    make && make install && \
    mkdir -p /work


VOLUME ["/work"]

ENV PATH /opt/ansible/ansible/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin
ENV PYTHONPATH /opt/ansible/ansible/lib
ENV ANSIBLE_LIBRARY /opt/ansible/ansible/library

WORKDIR /work

ENTRYPOINT ["ansible-playkit"]
