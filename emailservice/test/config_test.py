import os
import unittest
from emailservice import config


class ConfigTest(unittest.TestCase):

    def test_config(self):
        path = config.Config.get_filename()
        self.assertTrue(os.path.isfile(path), "config file not found")
