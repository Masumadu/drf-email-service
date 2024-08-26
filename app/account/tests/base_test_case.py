import uuid
from unittest import mock

from app.account.controller import MailAccountController
from app.account.models import MailAccountModel
from app.account.repository import MailAccountRepository
from tests import BaseTestCase

from .test_data import MailAccountTestData


class MailAccountTestCase(BaseTestCase):
    def setup_test_data(self):
        self.mail_account_test_data = MailAccountTestData()
        self.mail_account_model = MailAccountModel.objects.create(
            **self.mail_account_test_data.existing_mail_account
        )
        super().setup_test_data()
        self.token = {
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
        }

    def instantiate_classes(self):
        """This is where all classes are instantiated for the test"""
        self.mail_account_repository = MailAccountRepository()
        self.mail_account_controller = MailAccountController(
            mail_account_repository=self.mail_account_repository,
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
