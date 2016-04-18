FROM ansible/ansible:ubuntu1404
MAINTAINER Oleg Poyaganov <oleg@poyaganov.com>

ADD . /opt/src

RUN cd /opt/src && \
    python setup.py install && \
    pip install -e "git+https://github.com/ansible/ansible.git@v2.0.2.0-0.4.rc4#egg=ansible" --upgrade && \
    rm -rf /opt/src && \
    mkdir -p /work

VOLUME ["/work"]

WORKDIR /work

ENTRYPOINT ["ansible-playkit"]
