import pinject
from celery import shared_task

from app.delivery.repository import MailDeliveryRepository
from core.interfaces import MailMailAttribute
from core.log import logger
from core.services import MailService

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[MailService, MailDeliveryRepository],
)
mail_service: MailService = obj_graph.provide(MailService)


@shared_task()
def send_mail_task(mail_attr: MailMailAttribute, mail_record: dict):
    """Sends an email when the feedback form has been submitted."""
    logger.info("Task [send_mail_task | processing]")
    if mail_service.send(mail_attribute=mail_attr, **mail_record):
        logger.error("Task [send_email_task | error]\n")
    else:
        logger.info("Task [send_email_task| successful]\n")
    return "Task [send_mail_task | end]"
