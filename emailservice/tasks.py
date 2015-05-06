__author__ = 'brianrefsdal'

import os
import logging
from celery import Celery
import mailgunapi
import mandrillapi

logger = logging.getLogger("taskworker")

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis')

@celery.task
def send(to, subject, msg, retry=0):
    logger.info("sending to MailGun")
    mailgun_respcode, mailgun_message = mailgunapi.MailGunApi.send(to, subject, msg)
    if int(mailgun_respcode) != 200:
        mandrill_resp = mandrillapi.MandrillApi.send(to, subject, msg)

        if mandrill_resp['status'] != 'sent':
            if retry > 1:
                logger.error("Connect to mailgun or mandrill after {0} attempts...".format(retry))
                return

            logger.error("Cannot connect to mailgun or mandrill, retrying...")
            send(to, subject, msg, retry + 1)


if __name__ == "__main__":
    celery.start()