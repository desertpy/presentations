FROM ubuntu:14.04
MAINTAINER  Austin Godber <godber@uberhip.com>
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get install -y build-essential python-setuptools python-dev libyaml-dev && \
  easy_install pip
ADD . /code
RUN pip install -r /code/requirements.txt
EXPOSE 5000
WORKDIR /code
CMD ["rqworker"]
