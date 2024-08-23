import uuid

from django.core.files.storage import storages
from django.db import models

from core.models import BaseModel


# Create your models here.
class MailTemplateModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_id = models.UUIDField(null=False, db_index=True)
    name = models.CharField(null=False, db_index=True)
    placeholders = models.JSONField(null=True)
    file = models.FileField(null=True, blank=True, storage=storages["minio"])
    file_system_id = models.CharField(null=True)

    class Meta:
        db_table = "mail_templates"
        ordering = ["created_at"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
