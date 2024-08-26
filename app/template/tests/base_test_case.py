import glob
import os
import uuid
from unittest import mock

from django.conf import settings

from app.template.controller import MailTemplateController
from app.template.models import MailTemplateModel
from app.template.repository import MailTemplateRepository
from tests import BaseTestCase

from .test_data import MailTemplateTestData


class MailTemplateTestCase(BaseTestCase):
    def setup_test_data(self):
        self.mail_template_test_data = MailTemplateTestData()
        self.mail_template_model = MailTemplateModel.objects.create(
            **self.mail_template_test_data.existing_template()
        )
        super().setup_test_data()
        self.token = {
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
        }

    def instantiate_classes(self):
        """This is where all classes are instantiated for the test"""
        self.mail_template_repository = MailTemplateRepository()
        self.mail_template_controller = MailTemplateController(
            mail_template_repository=self.mail_template_repository,
        )
        super().instantiate_classes()

    def setup_patches(self):
        """This is where all mocked object are setup for the test"""
        decode = mock.patch(
            "core.utils.auth.KeycloakOpenID.decode_token",
        )
        self.addCleanup(decode.stop)
        self.jwt_decode = decode.start()
        super().setup_patches()

    # noinspection PyMethodMayBeStatic
    def mock_decode_token(self, *args, **kwargs):
        return {"preferred_username": str(uuid.uuid4())}

    def tearDown(self):
        files = glob.glob(os.path.join(settings.MEDIA_ROOT, "*.html"))
        for file in files:
            os.remove(file)
