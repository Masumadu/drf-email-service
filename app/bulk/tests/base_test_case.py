import os
from unittest import mock

from django.conf import settings

from app.account.models import MailAccountModel
from app.account.repository import MailAccountRepository
from app.account.tests import MailAccountTestData
from app.bulk.controller import BulkMailController
from app.bulk.models import BulkMailModel
from app.bulk.repository import BulkMailRepository
from app.delivery.repository import MailDeliveryRepository
from app.template.controller import MailTemplateController
from app.template.models import MailTemplateModel
from app.template.repository import MailTemplateRepository
from app.template.tests import MailTemplateTestData
from tests import BaseTestCase

from .test_data import BulkMailTestData


class BulkMailTestCase(BaseTestCase):
    def setup_test_data(self):
        self.bulk_mail_test_data = BulkMailTestData()
        self.bulk_mail_model = BulkMailModel.objects.create(
            **self.bulk_mail_test_data.existing_mail
        )
        self.mail_account_test_data = MailAccountTestData()
        self.mail_account_model = MailAccountModel.objects.create(
            **self.mail_account_test_data.existing_mail_account
        )
        self.mail_template_test_data = MailTemplateTestData()
        self.mail_template_model = MailTemplateModel.objects.create(
            **self.mail_template_test_data.existing_template(self.bulk_mail_model.id)
        )
        with open(
            f"{settings.MEDIA_ROOT}/templates/{self.mail_template_model.name}", "w"
        ) as buffer:
            buffer.write("<html><body><h1>test</h1></body></html>")
        super().setup_test_data()
        self.token = {
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
        }

    def instantiate_classes(self):
        """This is where all classes are instantiated for the test"""
        self.mail_account_repository = MailAccountRepository()
        self.bulk_mail_repository = BulkMailRepository()
        self.mail_template_repository = MailTemplateRepository()
        self.mail_delivery_repository = MailDeliveryRepository()
        self.mail_template_controller = MailTemplateController(
            mail_template_repository=self.mail_template_repository,
        )
        self.bulk_mail_controller = BulkMailController(
            mail_account_repository=self.mail_account_repository,
            mail_delivery_repository=self.mail_delivery_repository,
            mail_template_controller=self.mail_template_controller,
            bulk_mail_repository=self.bulk_mail_repository,
        )
        super().instantiate_classes()

    def setup_patches(self):
        """This is where all mocked object are setup for the test"""
        decode = mock.patch(
            "core.utils.auth.KeycloakOpenID.decode_token",
        )
        self.addCleanup(decode.stop)
        self.jwt_decode = decode.start()
        task = mock.patch(
            "core.tasks.send_mail.send_mail_task.apply_async",
        )
        self.addCleanup(task.stop)
        self.celery_task = task.start()
        super().setup_patches()

    # noinspection PyMethodMayBeStatic
    def mock_decode_token(self, *args, **kwargs):
        return {"preferred_username": str(self.bulk_mail_model.id)}

    def tearDown(self):
        os.remove(f"{settings.MEDIA_ROOT}/templates/{self.mail_template_model.name}")
