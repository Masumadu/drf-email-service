import json
import os
import sys
import uuid

import pinject
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger as loguru_logger

# Add "app" root to PYTHONPATH so we can import from app i.e. from app import create_app.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")


if __name__ == "__main__":
    import django

    django.setup()
    from django.conf import settings

    try:
        loguru_logger.info("CONNECTING TO KAFKA SERVER")
        consumer = KafkaConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
            group_id=settings.KAFKA_CONSUMER_GROUP,
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="SCRAM-SHA-256",
            sasl_plain_username=settings.KAFKA_SERVER_USERNAME,
            sasl_plain_password=settings.KAFKA_SERVER_PASSWORD,
            enable_auto_commit=False,
        )
    except KafkaError as exc:
        loguru_logger.error(f"error({exc}) occurred while connecting to kafka")
    else:
        consumer.subscribe(settings.KAFKA_SUBSCRIPTIONS)
        loguru_logger.info(f"Event Subscription List: {settings.KAFKA_SUBSCRIPTIONS}")
        loguru_logger.info("AWAITING MESSAGES\n")
        from app.account.controller import (
            MailAccountController,
            MailAccountRepository,
        )
        from app.bulk.controller import (
            BulkMailController,
            BulkMailRepository,
        )
        from app.delivery.repository import MailDeliveryRepository
        from app.template.controller import (
            MailTemplateController,
            MailTemplateRepository,
            ObjectStorageLogRepository,
        )
        from core.exceptions import AppExceptionCase

        for msg in consumer:
            data = json.loads(msg.value)
            message_id = str(uuid.uuid4())
            loguru_logger.info(f"[consuming | message | {msg}]")
            obj_graph = pinject.new_object_graph(
                modules=None,
                classes=[
                    BulkMailController,
                    BulkMailRepository,
                    MailTemplateRepository,
                    MailTemplateController,
                    MailDeliveryRepository,
                    MailAccountController,
                    MailAccountRepository,
                    ObjectStorageLogRepository,
                ],
            )
            bulk_mail_controller: BulkMailController = obj_graph.provide(
                BulkMailController
            )
            try:
                loguru_logger.info("[processing | message]")
                bulk_mail_controller.consumer_send_mail(obj_data=data)
                loguru_logger.success("[message | successfully | processed]")
            except AppExceptionCase as exc:
                loguru_logger.error(f"[message | processing | failed | {exc}]")
            finally:
                consumer.commit()
                loguru_logger.success("[message | successfully | consumed]")
