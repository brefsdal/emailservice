import os
import logging
from celery import Celery
from emailservice.mailgunapi import MailGunApi
from emailservice.mandrillapi import MandrillApi

logger = logging.getLogger("taskworker")

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis')


@celery.task(bind=True, name="emailservice.tasks.send", default_retry_delay=5 * 60)
def send(self, to, subject, msg):
    """

    :param to: list of email addresses
    :param subject: string
    :param msg: string
    :param retry: integer
    :return:
    """

    logger.info("sending to Mailgun")
    mailgun_respcode, mailgun_message = MailGunApi.send(to, subject, msg)
    if int(mailgun_respcode) != 200:
        logger.info("sending to Mandrill")
        mandrill_resp = MandrillApi.send(to, subject, msg)
        if mandrill_resp['status'] != 'sent':
            logger.error("Cannot connect to Mailgun or Mandrill, retrying...")
            # Default number of reties is 3
            # Retry delay is 5 minutes
            self.retry()


if __name__ == "__main__":
    celery.start()
