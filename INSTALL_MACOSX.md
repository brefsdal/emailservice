Installing on Mac OSX
=====================

Steps:

   1. Download and install Python 2.7.9 64-bit dmg from python.org

   2. Set PATH variable to include `/Library/Frameworks/Python.framework/Versions/2.7/bin`

   3. Install virtualenv with `easy_install virtualenv`

   4. Download and install rabbitMQ `brew install rabbitmq`

   5. Download and install Redis `brew install redis`

   6. Configure virtualenv with `virtualenv env`

   7. Activate virtualenv with `. env/bin/activate`

   8. Install all dependencies with pip and requirements.txt `pip install -r requirements.txt`

   9. Install pycurl (Optional) `PYCURL_CURL_CONFIG=/usr/bin/curl-config ARCHFLAGS=-arch x86_64`
   