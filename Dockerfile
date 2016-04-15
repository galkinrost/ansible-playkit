FROM ansible/ansible:ubuntu1404
MAINTAINER Oleg Poyaganov <oleg@poyaganov.com>

ADD . /opt/src

RUN cd /opt/src && \
    python setup.py install && \
    rm -rf /opt/src && \
    mkdir -p /work

VOLUME ["/work"]

ENTRYPOINT ["ansible-playkit"]
CMD ["play"]
