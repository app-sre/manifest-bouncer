FROM registry.access.redhat.com/ubi8/python-38

ADD . .

RUN python setup.py install

ENTRYPOINT [ "manifest-bouncer" ]
