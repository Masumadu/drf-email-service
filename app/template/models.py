import uuid

from django.db import models

from core.models import BaseModel


# Create your models here.
class ObjectStorageLogModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.UUIDField(null=False, db_index=True)
    bucket = models.CharField(null=False)
    key = models.CharField(null=False, unique=True, db_index=True)
    name = models.CharField(null=False)
    description = models.CharField(null=False)
    content_type = models.CharField(null=False)
    meta_data = models.JSONField(null=True)

    class Meta:
        db_table = "object_storage_logs"
        ordering = ["created_at"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MailTemplateModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_id = models.UUIDField(null=False, db_index=True)
    name = models.CharField(null=False, db_index=True)
    placeholders = models.JSONField(null=True)
    file_sys_path = models.CharField(db_index=True)
    object_storage = models.ForeignKey(
        to=ObjectStorageLogModel, on_delete=models.DO_NOTHING, db_index=True
    )

    class Meta:
        db_table = "mail_templates"
        ordering = ["created_at"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
