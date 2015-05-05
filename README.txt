04/30/2015

Email Service

Installing on Mac OSX

1)
Download and install Python 2.7.9 64-bit dmg from python.org

2)
Set PATH variable to include
/Library/Frameworks/Python.framework/Versions/2.7/bin

3)
Install virtualenv with 
easy_install virtualenv

4)
Download and install rabbitMQ
brew install rabbitmq

5)
Download and install Redis

6)
Install virtualenv using pip

7)
Configure virtualenv with
% virtualenv env

8) Activate virtualenv with
% . env/bin/activate

9)
Install all dependencies with pip and requirements.txt
% pip install -r requirements.txt

10) Install pycurl
PYCURL_CURL_CONFIG=/usr/bin/curl-config
ARCHFLAGS=-arch x86_64