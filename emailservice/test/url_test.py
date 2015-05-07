import unittest
import urllib


class UrlTest(unittest.TestCase):

    def test_url(self):

        result = urllib.urlopen("http://127.0.0.1:8000/send")
        data = result.fp.read()
        self.assertEqual(result.code, 200, 'status code failed')
        self.assertEqual(data, '{"to": "somebody@gmail.com", "text": "this is the body", "subject": "test subject"}', 'url test failed')
