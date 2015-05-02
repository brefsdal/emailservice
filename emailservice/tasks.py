__author__ = 'brianrefsdal'


import os
import time
import logging
from datetime import datetime

from celery import Celery

from emailservice import mailgunapi
from emailservice import mandrillapi

logger = logging.getLogger("taskworker")

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis')

# @celery.task
# def send(to, subject, msg):
#     logger.info("sending to MailGun")
#     return mailgun.MailGunApi.send(to, subject, msg)

@celery.task
def send(to, subject, msg):
    return mandrillapi.MandrillApi.send(to, subject, msg)


if __name__ == "__main__":
    celery.start()