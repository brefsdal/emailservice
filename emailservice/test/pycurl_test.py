import unittest
# import sys
import pycurl
import cStringIO


class PycurlTest(unittest.TestCase):

    def test_pycurl(self):

        cstring = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, "http://127.0.0.1:8000/send")
        c.setopt(pycurl.WRITEDATA, cstring)
        c.setopt(pycurl.CONNECTTIMEOUT, 30)
        # try:
        #     c.perform()
        # except:
        #     import traceback
        #     traceback.print_exc(file=sys.stderr)
        #     sys.stderr.flush()
        c.perform()
        result = str(cstring.getvalue())
        cstring.close()
        c.close()
        self.assertEqual(result, '{"to": "somebody@gmail.com", "text": "this is the body", "subject": "test subject"}', 'pycurl failed')
