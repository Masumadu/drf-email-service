from django.test import tag

from app.bulk.models import BulkMailModel

from .base_test_case import BulkMailTestCase


@tag("app.bulk.model")
class TestBulkMailModel(BulkMailTestCase):
    def test_single_mail_model(self):
        self.assertEqual(BulkMailModel.objects.count(), 1)
        mail = BulkMailModel.objects.get(pk=self.bulk_mail_model.id)
        self.assertIsInstance(mail, BulkMailModel)
        self.assertTrue(hasattr(mail, "id"))
        self.assertTrue(hasattr(mail, "user_id"))
        self.assertTrue(hasattr(mail, "sender"))
        self.assertTrue(hasattr(mail, "name"))
        self.assertTrue(hasattr(mail, "recipients"))
        self.assertTrue(hasattr(mail, "subject"))
        self.assertTrue(hasattr(mail, "html_body"))
        self.assertTrue(hasattr(mail, "text_body"))
        self.assertTrue(hasattr(mail, "is_scheduled"))
        self.assertTrue(hasattr(mail, "scheduled_date"))
        self.assertTrue(hasattr(mail, "created_at"))
        self.assertTrue(hasattr(mail, "created_by"))
        self.assertTrue(hasattr(mail, "updated_at"))
        self.assertTrue(hasattr(mail, "updated_by"))
        self.assertTrue(hasattr(mail, "deleted_at"))
        self.assertTrue(hasattr(mail, "deleted_by"))
