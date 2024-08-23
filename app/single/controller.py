from amqp import exceptions as amqp_exc
from kombu import exceptions as kombu_exc
from rest_framework.request import Request

from app.account.repository import MailAccountRepository
from app.delivery.repository import MailDeliveryRepository
from app.template.controller import MailTemplateController
from core.exceptions import AppException
from core.interfaces import MailMailAttribute
from core.tasks import send_mail_task
from core.utils import remove_none_fields
from core.utils.constants import MailDeliveryStatusEnum

from .repository import SingleMailRepository
from .serializer import (
    SendSingleMailSerializer,
    SendSingleMailTemplateSerializer,
    SingleMailResponseSerializer,
    SingleMailSerializer,
)


class SingleMailController:
    def __init__(
        self,
        single_mail_repository: SingleMailRepository,
        mail_account_repository: MailAccountRepository,
        mail_delivery_repository: MailDeliveryRepository,
        mail_template_controller: MailTemplateController,
    ):
        self.single_mail_repository = single_mail_repository
        self.mail_account_repository = mail_account_repository
        self.mail_delivery_repository = mail_delivery_repository
        self.mail_template_controller = mail_template_controller

    def view_all_mails(self, request: Request):
        paginator, result = self.single_mail_repository.index(request)
        serializer = SingleMailSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def send_mail(self, request: Request):
        serializer = SendSingleMailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            obj_data, mail_record = self.create_mail_record(
                obj_data=remove_none_fields(
                    data={"user_id": request.user.get("preferred_username"), **data}
                )
            )
            mail_delivery = self.create_delivery_record(
                user_id=request.user.get("preferred_username"), mail_id=mail_record.id
            )
            self.create_task(
                obj_data={
                    "mail_id": mail_record.id,
                    "sender_address": obj_data.get("sender"),
                    "sender_name": obj_data.get("name"),
                    "password": obj_data.get("password"),
                    "recipient": obj_data.get("recipient"),
                    "subject": obj_data.get("subject"),
                    "delivery_id": mail_delivery.id,
                    "html_body": obj_data.get("html_body"),
                    "text_body": obj_data.get("text_body"),
                },
            )
            return SingleMailResponseSerializer(
                {"id": mail_record.id, "is_success": True}
            )
        raise AppException.ValidationException(error_message=serializer.errors)

    def get_mail(self, obj_id: str):
        return SingleMailSerializer(self.single_mail_repository.find_by_id(obj_id))

    def send_mail_with_template(self, request: Request):
        serializer = SendSingleMailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            message, redacted_message = self.mail_template_controller.generate_message(
                query_template=remove_none_fields(
                    {
                        "id": data.get("template_id"),
                        "user_id": request.user.get("preferred_username"),
                        "name": data.get("template_name"),
                        "is_deleted": False,
                    }
                ),
                keywords=data.get("keywords", {}),
            )
            obj_data, mail_record = self.create_mail_record(
                obj_data=remove_none_fields(
                    data={"user_id": request.user.get("preferred_username"), **data}
                )
            )
            mail_delivery = self.create_delivery_record(
                user_id=request.user.get("preferred_username"), mail_id=mail_record.id
            )
            self.create_task(
                obj_data={
                    "mail_id": mail_record.id,
                    "sender_address": obj_data.get("sender"),
                    "sender_name": obj_data.get("name"),
                    "password": obj_data.get("password"),
                    "recipient": obj_data.get("recipient"),
                    "subject": obj_data.get("subject"),
                    "delivery_id": mail_delivery.id,
                    "html_body": message,
                },
            )
            return SingleMailResponseSerializer(
                {"id": mail_record.id, "is_success": True}
            )
        raise AppException.ValidationException(error_message=serializer.errors)

    def delete_mail(self, obj_id: str):
        self.single_mail_repository.delete_by_id(obj_id)
        return None

    def create_mail_record(self, obj_data: dict):
        account = self.mail_account_repository.find(
            filter_param={"mail_address": obj_data.get("sender"), "is_deleted": False}
        )
        obj_data["name"] = obj_data.get("name", account.sender_name)
        obj_data["password"] = account.password
        mail = self.single_mail_repository.create(
            obj_data={
                "user_id": obj_data.get("user_id"),
                "sender": obj_data.get("sender"),
                "recipient": obj_data.get("recipient"),
                "subject": obj_data.get("subject"),
                "html_body": obj_data.get("html_body"),
                "text_body": obj_data.get("text_body"),
            }
        )
        return obj_data, mail

    def create_delivery_record(self, user_id: str, mail_id: str):
        return self.mail_delivery_repository.create(
            obj_data={
                "user_id": user_id,
                "single_mail_id": mail_id,
                "status": MailDeliveryStatusEnum.not_sent_to_provider.value,
            }
        )

    # noinspection PyMethodMayBeStatic
    def create_task(self, obj_data: dict):
        try:
            send_mail_task.apply_async(
                kwargs={
                    "mail_attr": MailMailAttribute(
                        sender_address=obj_data.get("sender_address"),
                        sender_name=obj_data.get("sender_name"),
                        password=obj_data.get("password"),
                        recipient=obj_data.get("recipient"),
                        subject=obj_data.get("subject"),
                        html_body=obj_data.get("html_body"),
                        text_body=obj_data.get("text_body"),
                    ),
                    "mail_record": {
                        "delivery_id": obj_data.get("delivery_id"),
                        "single_mail_id": obj_data.get("mail_id"),
                    },
                },
                kwargsrepr="",
            )
        except (kombu_exc.KombuError, amqp_exc.AMQPError) as exc:
            raise AppException.InternalServerException(
                error_message=f"CeleryBrokerError({exc})"
            ) from exc
        return None
