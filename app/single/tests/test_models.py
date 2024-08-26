from django.test import tag

from app.single.models import SingleMailModel

from .base_test_case import SingleMailTestCase


@tag("app.single.model")
class TestSingleMailModel(SingleMailTestCase):
    def test_single_mail_model(self):
        self.assertEqual(SingleMailModel.objects.count(), 1)
        mail = SingleMailModel.objects.get(pk=self.single_mail_model.id)
        self.assertIsInstance(mail, SingleMailModel)
        self.assertTrue(hasattr(mail, "id"))
        self.assertTrue(hasattr(mail, "user_id"))
        self.assertTrue(hasattr(mail, "sender"))
        self.assertTrue(hasattr(mail, "name"))
        self.assertTrue(hasattr(mail, "recipient"))
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
