from datetime import datetime, timezone
from typing import Union

from django.core import mail as django_mail
from django.core.mail import EmailMultiAlternatives

from app.account.models import MailAccountModel
from app.delivery.repository import MailDeliveryRepository
from core.exceptions import AppException
from core.interfaces import MailMailAttribute, MailServiceInterface
from core.log import logger
from core.utils.constants import MailDeliveryStatusEnum


class MailService(MailServiceInterface):
    client = "QuantumMailServer"

    def __init__(self, mail_delivery_repository: MailDeliveryRepository):
        self.mail_delivery_repository = mail_delivery_repository
        self.error = False

    def send(self, mail_attribute: MailMailAttribute, **kwargs):
        sender_address = mail_attribute.get("sender_address")
        sender_name = mail_attribute.get("sender_name")
        recipients = self._recipients(mail_attribute.get("recipient"))
        try:
            with django_mail.get_connection(
                username=sender_address,
                password=MailAccountModel.decrypt_text(
                    passkey=sender_address,
                    encrypted_text=mail_attribute.get("password"),
                ),
            ) as connection:
                for addresses in self.send_in_batches(recipients=recipients, size=100):
                    try:
                        mail = EmailMultiAlternatives(
                            subject=mail_attribute.get("subject"),
                            body=mail_attribute.get("text_body"),
                            from_email=f"{sender_name} <{sender_address}>",
                            to=addresses,
                            connection=connection,
                        )
                        mail.attach_alternative(
                            mail_attribute.get("html_body"), "text/html"
                        )
                        mail.send()
                        self.update_delivery_report(
                            obj_data={
                                "date_sent": datetime.now(timezone.utc),
                                "delivery_id": kwargs.get("delivery_id"),
                                "single_mail_id": kwargs.get("single_mail_id"),
                                "bulk_mail_id": kwargs.get("bulk_mail_id"),
                                "status": MailDeliveryStatusEnum.sent_to_provider.value,
                                "recipients": len(addresses),
                            }
                        )
                    except Exception as exc:
                        self.error = True
                        self.update_delivery_report(
                            obj_data={
                                "delivery_id": kwargs.get("delivery_id"),
                                "single_mail_id": kwargs.get("single_mail_id"),
                                "bulk_mail_id": kwargs.get("bulk_mail_id"),
                                "status": MailDeliveryStatusEnum.not_sent_to_provider.value,
                                "recipients": len(addresses),
                                "comment": f"{exc.args}",
                            }
                        )
                        logger.error(f"{exc}")

        except Exception as exc:
            self.error = True
            self.update_delivery_report(
                obj_data={
                    "delivery_id": kwargs.get("delivery_id"),
                    "single_mail_id": kwargs.get("single_mail_id"),
                    "bulk_mail_id": kwargs.get("bulk_mail_id"),
                    "status": MailDeliveryStatusEnum.not_sent_to_provider.value,
                    "recipients": len(recipients),
                    "comment": f"{exc.args}",
                }
            )
            logger.error(f"{exc}")

        return self.error

    def update_delivery_report(self, obj_data: dict):
        try:
            self.mail_delivery_repository.update_by_id(
                obj_id=obj_data.get("delivery_id"),
                obj_data={
                    "status": obj_data.get("status"),
                    "provider": self.client,
                    "single_mail_id": obj_data.get("single_mail_id"),
                    "bulk_mail_id": obj_data.get("bulk_mail_id"),
                    "total_recipients": obj_data.get("recipients"),
                    "comment": obj_data.get("comment"),
                    "date_sent": obj_data.get("date_sent"),
                },
            )
        except AppException.NotFoundException:
            logger.warning(f"DeliveryReportUpdateError({obj_data})")

    # noinspection PyMethodMayBeStatic
    def send_in_batches(self, recipients: list, size: int):
        for _ in range(0, len(recipients), size):
            yield recipients[_ : size + _]

    def _recipients(self, recipient: Union[list, str]):
        return recipient if isinstance(recipient, list) else [recipient]
