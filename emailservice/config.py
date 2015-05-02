__author__ = 'brianrefsdal'


import os
import ConfigParser
import emailservice


class Config(object):

    config = None

    @classmethod
    def get_filename(cls, filename="emailservice.cfg"):
        home_dir = os.environ.get("HOME")
        local_file = os.path.join(home_dir, ".{0}".format(filename))
        if os.path.isfile(local_file):
            return local_file
        path = os.path.join(os.path.dirname(emailservice.__file__), filename)
        return path

    @classmethod
    def get_config(cls):
        if cls.config is None:
            parser = ConfigParser.ConfigParser()
            path = cls.get_filename()
            parser.readfp(open(path))
            cls.config = parser
            return cls.config
        else:
            cls.config
