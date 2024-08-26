from django.test import tag

from app.template.models import MailTemplateModel

from .base_test_case import MailTemplateTestCase


@tag("app.template.model")
class TestTemplateModel(MailTemplateTestCase):
    def test_mail_template_model(self):
        self.assertEqual(MailTemplateModel.objects.count(), 1)
        template = MailTemplateModel.objects.get(pk=self.mail_template_model.id)
        self.assertIsInstance(template, MailTemplateModel)
        self.assertTrue(hasattr(template, "id"))
        self.assertTrue(hasattr(template, "user_id"))
        self.assertTrue(hasattr(template, "name"))
        self.assertTrue(hasattr(template, "placeholders"))
        self.assertTrue(hasattr(template, "file"))
        self.assertTrue(hasattr(template, "file_system_id"))
        self.assertTrue(hasattr(template, "created_at"))
        self.assertTrue(hasattr(template, "created_by"))
        self.assertTrue(hasattr(template, "updated_at"))
        self.assertTrue(hasattr(template, "updated_by"))
        self.assertTrue(hasattr(template, "deleted_at"))
        self.assertTrue(hasattr(template, "deleted_by"))
