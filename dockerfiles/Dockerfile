FROM python:3.7.4

ADD . /package
WORKDIR /package

RUN python setup.py install

ENTRYPOINT [ "manifest-bouncer" ]
