FROM python:3.8.2-buster

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y --no-install-recommends install \
    build-essential \
    git \
    curl \
    wget \
    sudo \
    net-tools \
    gnupg dos2unix vim

RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

RUN apt-get -y update
RUN apt-get install -y mongodb-org-shell

#
# the display setting does not work
#
# CMD export DISPLAY =":0.0"

RUN pip install pip -U
RUN pip install cloudmesh-installer

RUN mkdir cm
WORKDIR cm

RUN cloudmesh-installer get cms cloud openstack aws azure

RUN mkdir $HOME/.cloudmesh
RUN mkdir $HOME/.ssh

COPY init.sh /
RUN dos2unix /init.sh
RUN chmod +x /init.sh

ENTRYPOINT /bin/bash /init.sh; /bin/bash

#docker run --rm -d -v /aux/github/cm/docker/mongo_data:/data/db -p 127.0.0.1:27017:27017/tcp --name mongos mongo:4.2
#docker run --rm -it -v /aux/github/cm/docker/cloudmesh_home:/root/.cloudmesh -v ~/.ssh:/root/.ssh --net host --name cms-container cloudmesh-cms
