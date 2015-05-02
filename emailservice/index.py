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

import tasks


#HOST='127.0.0.1'
HOST = 'localhost'
PORT = 8000
SECRET = str(base64.b64encode(hashlib.sha256(str(random.random())).digest()))

define("port", default=PORT, help="run on the given port", type=int)
define("host", default=HOST, help="run on the given address", type=str)

logger = logging.getLogger("emailhandler")


class EmailAsyncHandler(RequestHandler):

    #@asynchronous
    # def get(self):
    #     data = {
    #         'to': 'somebody@gmail.com',
    #         'subject': 'test subject',
    #         'text': 'this is the body'
    #     }
    #     self.write(json.dumps(data))

    @asynchronous
    def post(self):
        if len(self.request.body) > 0:
            logger.info("request body => {0}".format(self.request.body))
            obj = json.loads(self.request.body)
            logger.info("json body => {0}".format(obj))
            tasks.send.apply_async(args=[obj['to'], obj['subject'], obj['text']], callback=self.on_result)


    def on_result(self, response):
        self.write(str(response.result))
        self.finish()


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
