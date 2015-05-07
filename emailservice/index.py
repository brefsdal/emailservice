#!/usr/bin/env python

import json
import logging

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import RequestHandler, asynchronous
from tornado.options import define, options
from validate_email import validate_email

import emailservice.tasks


HOST = 'localhost'
PORT = 8000

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
        if not isinstance(obj['to'], (tuple, list)):
            return self.error(400, "'to' must be a list of valid email addresses")
        for email in obj['to']:
            if not validate_email(email):
                return self.error(400, "'to' {0} must be a valid email address".format(email))
        if not obj['text']:
            return self.error(400, "'text' body cannot be empty")
        if not obj['subject']:
            return self.error(400, "'subject' line cannot be empty")
        if len(obj['text']) > 1048576:
            return self.error(400, "'text' body cannot be larger than 1MB")
        if len(obj['subject']) > 78:
            return self.error(400, "'subject' line cannot be larger than 78 characters")
        # TODO: Implement file attachments
        result = emailservice.tasks.send.apply_async(args=[obj['to'], obj['subject'], obj['text']])
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
        tornado.web.Application.__init__(self, handlers)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port, options.host)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
