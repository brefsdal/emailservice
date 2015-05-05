__author__ = 'brianrefsdal'

from mandrill import Mandrill
from emailservice.config import Config


class MandrillApi(object):

    def __init__(self):
        pass

    message = {
        'attachments': [],
        'auto_html': None,
        'auto_text': None,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Example Name',
        'global_merge_vars': [],
        'google_analytics_campaign': '',
        'google_analytics_domains': [],
        'headers': {},
        'html': '',
        'images': [],
        'important': False,
        'inline_css': None,
        'merge': False,
        'merge_language': 'mailchimp',
        'merge_vars': [],
        'metadata': {},
        'preserve_recipients': None,
        'recipient_metadata': [],
        'return_path_domain': None,
        'signing_domain': None,
        'subaccount': '',
        'subject': '',
        'tags': [],
        'text': '',
        'to': [{'email': '', 'type': 'to'}],
        'track_clicks': None,
        'track_opens': None,
        'tracking_domain': None,
        'url_strip_qs': None,
        'view_content_link': None}

    @classmethod
    def send(cls, to, subject, msg):
        config = Config.get_config()
        apikey = config.get("mandrill", "apikey")
        subaccount = config.get("mandrill", "subaccount")
        client = Mandrill(apikey)
        data = cls.message.copy()
        data['text'] = msg
        data['subject'] = subject
        data['to'][0]['email'] = to
        data['subaccount'] = subaccount
        result = client.messages.send(message=data, async=False, ip_pool='Main Pool')
        return result[0]
