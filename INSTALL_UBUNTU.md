Installing on Ubuntu 
====================

AWS Ubuntu 14.04.2 LTS

Python 2.7.6 installed

Need to install

easy_install
virtualenv
pip

rabbitmq
https://www.rabbitmq.com/install-debian.html

redis
https://www.linode.com/docs/databases/redis/redis-on-ubuntu-12-04-precise-pangolin


# commands

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install htop emacs ngrep bwm-ng tcpdump gcc g++ rabbitmq-server redis-server python-pip libcurl4-openssl-dev python2.7-dev git --fix-missing

sudo pip install virtualenv

# enable rabbitmq web interface

rabbitmq-plugins enable rabbitmq_management


# install emailservice
pip install -U 'git+https://github.com/brefsdal/emailservice'


# copy the upstart scripts to /etc/init/

# install the emailservice.cfg in the home dir