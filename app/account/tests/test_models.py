from django.test import tag

from app.account.models import MailAccountModel

from .base_test_case import MailAccountTestCase


@tag("app.account.model")
class TestAccountModel(MailAccountTestCase):
    def test_mail_account_model(self):
        self.assertEqual(MailAccountModel.objects.count(), 1)
        account = MailAccountModel.objects.get(pk=self.mail_account_model.id)
        self.assertIsInstance(account, MailAccountModel)
        self.assertTrue(hasattr(account, "id"))
        self.assertTrue(hasattr(account, "user_id"))
        self.assertTrue(hasattr(account, "mail_address"))
        self.assertTrue(hasattr(account, "sender_name"))
        self.assertTrue(hasattr(account, "_password"))
        self.assertTrue(hasattr(account, "is_default"))
        self.assertTrue(hasattr(account, "created_at"))
        self.assertTrue(hasattr(account, "created_by"))
        self.assertTrue(hasattr(account, "updated_at"))
        self.assertTrue(hasattr(account, "updated_by"))
        self.assertTrue(hasattr(account, "deleted_at"))
        self.assertTrue(hasattr(account, "deleted_by"))
