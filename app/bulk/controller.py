from amqp import exceptions as amqp_exc
from kombu import exceptions as kombu_exc
from rest_framework.request import Request

from app.account.repository import MailAccountRepository
from app.delivery.repository import MailDeliveryRepository
from app.template.controller import MailTemplateController
from core.exceptions import AppException
from core.interfaces import MailMailAttribute
from core.tasks import send_mail_task

from .repository import BulkMailRepository
from .serializer import (
    BulkMailResponseSerializer,
    BulkMailSerializer,
    ConsumerSendBulkMailSerializer,
    SendBulkMailSerializer,
    SendBulkMailTemplateSerializer,
)


class BulkMailController:
    def __init__(
        self,
        bulk_mail_repository: BulkMailRepository,
        mail_account_repository: MailAccountRepository,
        mail_delivery_repository: MailDeliveryRepository,
        mail_template_controller: MailTemplateController,
    ):
        self.bulk_mail_repository = bulk_mail_repository
        self.mail_account_repository = mail_account_repository
        self.mail_delivery_repository = mail_delivery_repository
        self.mail_template_controller = mail_template_controller

    def view_all_mails(self, request: Request):
        paginator, result = self.bulk_mail_repository.index(request)
        serializer = BulkMailSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def send_mail(self, request: Request):
        serializer = SendBulkMailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            obj_data, mail_record = self.create_mail_record(
                user_id=request.user.get("preferred_username"), obj_data=data
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
                    "recipients": obj_data.get("recipients"),
                    "subject": obj_data.get("subject"),
                    "delivery_id": mail_delivery.id,
                    "html_body": obj_data.get("html_body"),
                    "text_body": obj_data.get("text_body"),
                },
            )
            return BulkMailResponseSerializer(
                {"id": mail_record.id, "is_success": True}
            )
        raise AppException.ValidationException(error_message=serializer.errors)

    def consumer_send_mail(self, obj_data: dict):
        serializer = ConsumerSendBulkMailSerializer(data=obj_data)
        if serializer.is_valid():
            data = serializer.validated_data
            obj_data, mail_record = self.create_mail_record(
                user_id=data.get("user_id"), obj_data=data
            )
            mail_delivery = self.create_delivery_record(
                user_id=data.get("user_id"), mail_id=mail_record.id
            )
            self.create_task(
                obj_data={
                    "mail_id": mail_record.id,
                    "sender_address": obj_data.get("sender"),
                    "sender_name": obj_data.get("name"),
                    "password": obj_data.get("password"),
                    "recipients": obj_data.get("recipients"),
                    "subject": obj_data.get("subject"),
                    "delivery_id": mail_delivery.id,
                    "html_body": obj_data.get("html_body"),
                    "text_body": obj_data.get("text_body"),
                },
            )
            return BulkMailResponseSerializer(
                {"id": mail_record.id, "is_success": True}
            )
        raise AppException.ValidationException(error_message=serializer.errors)

    def get_mail(self, obj_id: str):
        return BulkMailSerializer(self.bulk_mail_repository.find_by_id(obj_id))

    def send_mail_with_template(self, request: Request):
        serializer = SendBulkMailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            message, redacted_message = self.mail_template_controller.generate_message(
                query_template={
                    "user_id": request.user.get("preferred_username"),
                    "id": data.get("template_id"),
                    "name": data.get("template_name"),
                    "is_deleted": False,
                },
                keywords=data.get("keywords", {}),
            )
            obj_data, mail_record = self.create_mail_record(
                user_id=request.user.get("preferred_username"), obj_data=data
            )
            mail_delivery = self.create_delivery_record(
                mail_id=mail_record.id, user_id=request.user.get("preferred_username")
            )
            self.create_task(
                obj_data={
                    "mail_id": mail_record.id,
                    "sender_address": obj_data.get("sender"),
                    "sender_name": obj_data.get("name"),
                    "password": obj_data.get("password"),
                    "recipients": obj_data.get("recipients"),
                    "subject": obj_data.get("subject"),
                    "delivery_id": mail_delivery.id,
                    "html_body": message,
                },
            )
            return BulkMailResponseSerializer(
                {"id": mail_record.id, "is_success": True}
            )
        raise AppException.ValidationException(error_message=serializer.errors)

    def delete_mail(self, obj_id: str):
        self.bulk_mail_repository.delete_by_id(obj_id)
        return None

    def create_mail_record(self, user_id: str, obj_data: dict):
        account = self.mail_account_repository.find(
            filter_param={
                "user_id": user_id,
                "mail_address": obj_data.get("sender"),
                "is_deleted": False,
            }
        )
        obj_data["name"] = obj_data.get("name", account.sender_name)
        obj_data["password"] = account.password
        mail = self.bulk_mail_repository.create(
            obj_data={
                "user_id": user_id,
                "sender": obj_data.get("sender"),
                "recipients": obj_data.get("recipients"),
                "subject": obj_data.get("subject"),
            }
        )
        return obj_data, mail

    def create_delivery_record(self, user_id: str, mail_id: str):
        return self.mail_delivery_repository.create(
            obj_data={"user_id": user_id, "bulk_mail_id": mail_id}
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
                        recipient=obj_data.get("recipients"),
                        subject=obj_data.get("subject"),
                        html_body=obj_data.get("html_body"),
                        text_body=obj_data.get("text_body"),
                    ),
                    "mail_record": {
                        "delivery_id": obj_data.get("delivery_id"),
                        "bulk_mail_id": obj_data.get("mail_id"),
                    },
                },
                kwargsrepr="",
            )
        except (kombu_exc.KombuError, amqp_exc.AMQPError) as exc:
            raise AppException.InternalServerException(
                error_message=f"CeleryBrokerError({exc})"
            ) from exc
        return None
