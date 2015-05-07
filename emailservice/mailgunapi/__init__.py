# import json
# import pycurl
# import urllib
# import cStringIO
import requests
from emailservice.config import Config


class MailGunApi(object):

    @staticmethod
    def send(to, subject, msg):
        config = Config.get_config()
        apikey = config.get("mailgun", "apikey")
        sandbox = config.get("mailgun", "sandbox")
        url = 'https://api.mailgun.net/v3/sandbox{0}.mailgun.org/messages'.format(sandbox)
        data = {
            'from': 'Mailgun Sandbox <postmaster@sandbox{0}.mailgun.org>'.format(sandbox),
            'to[]': to,
            'subject': subject,
            'text': msg
        }
        user, password = apikey.split(":")
        response = requests.post(url, data, auth=(user, password))
        return response.status_code, response.json().get('message', '')

    # @staticmethod
    # def send(to, subject, msg):
    #     config = Config.get_config()
    #     apikey = config.get("mailgun", "apikey")
    #     sandbox = config.get("mailgun", "sandbox")
    #     url = 'https://api.mailgun.net/v3/sandbox{0}.mailgun.org/messages'.format(sandbox)
    #     data = {
    #         'from': 'Mailgun Sandbox <postmaster@sandbox{0}.mailgun.org>'.format(sandbox),
    #         'to': to,
    #         'subject': subject,
    #         'text': msg
    #     }
    #     form_data = urllib.urlencode(data)
    #     resp = urllib.urlopen(url, form_data)
    #     response = resp.fp.read()
    #     obj = {}
    #     if response:
    #         obj = json.dumps(response)
    #     message = obj.get('message', '')
    #     return resp.code, message
    #
    # @staticmethod
    # def send(to, subject, msg):
    #     config = Config.get_config()
    #     apikey = config.get("mailgun", "apikey")
    #     sandbox = config.get("mailgun", "sandbox")
    #     url = 'https://api.mailgun.net/v3/sandbox{0}.mailgun.org/messages'.format(sandbox)
    #     data = {
    #         'from': 'Mailgun Sandbox <postmaster@sandbox{0}.mailgun.org>'.format(sandbox),
    #         'to': to,
    #         'subject': subject,
    #         'text': msg
    #     }
    #     form_data = urllib.urlencode(data)
    #     cstring = cStringIO.StringIO()
    #     c = pycurl.Curl()
    #     c.setopt(pycurl.URL, url)
    #     c.setopt(pycurl.POSTFIELDS, form_data)
    #     c.setopt(pycurl.VERBOSE, 1)
    #     c.setopt(pycurl.USERPWD, apikey)
    #     c.setopt(pycurl.WRITEDATA, cstring)
    #     c.setopt(pycurl.CONNECTTIMEOUT, 30)
    #     c.perform()
    #     c.close()
    #     result = str(cstring.getvalue())
    #     cstring.close()
    #
    #     obj = {}
    #     if result:
    #         obj = json.dumps(result)
    #
    #     message = obj.get('message', '')
    #     return c.getinfo(pycurl.RESPONSE_CODE), message
