#!/usr/bin/env python

import os
import json
import os.path
import base64
import hashlib
import random
import logging

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import RequestHandler, asynchronous
from tornado.options import define, options
from validate_email import validate_email

from emailservice.tasks import send


#HOST='127.0.0.1'
HOST = 'localhost'
PORT = 8000
SECRET = str(base64.b64encode(hashlib.sha256(str(random.random())).digest()))

define("port", default=PORT, help="run on the given port", type=int)
define("host", default=HOST, help="run on the given address", type=str)

logger = logging.getLogger("emailhandler")


class EmailAsyncHandler(RequestHandler):

    def get(self):
        data = {
            'to': 'somebody@gmail.com',
            'subject': 'test subject',
            'text': 'this is the body'
        }
        self.write(json.dumps(data))

    def post(self):
        if not self.request.body:
            return self.error(400, "Empty request")
        logger.info("request body => {0}".format(self.request.body))
        try:
            obj = json.loads(self.request.body)
        except:
            return self.error(400, "Invalid json")
        logger.info("json body => {0}".format(obj))
        if 'to' not in obj or 'subject' not in obj or 'text' not in obj:
            return self.error(400, "Must include 'to', 'subject', and 'text'")
        if not validate_email(obj['to']):
            return self.error(400, "'to' must be a valid email address")
        result = send.apply_async(args=[obj['to'], obj['subject'], obj['text']])
        self.write({'task-id': result.task_id, 'state': result.state})

    def error(self, status_code, error_msg):
        self.clear()
        self.set_status(status_code)
        self.finish("<html><body>{0}</body></html>".format(error_msg))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/send", EmailAsyncHandler),
        ]
        settings = dict(
            cookie_secret=SECRET,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, options.host)
    ioloop = tornado.ioloop.IOLoop.instance()
    #celery = Celery("tasks", broker="amqp://")
    #celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis')
    #tcelery.setup_nonblocking_producer(celery_app=celery, io_loop=ioloop)
    ioloop.start()


if __name__ == "__main__":
    main()
