import uuid

from django.db import models

from core.models import BaseModel

# Create your models here.


class SingleMailModel(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_id = models.UUIDField(null=False, db_index=True)
    sender = models.CharField(null=False, db_index=True)
    name = models.CharField(null=False, db_index=True)
    recipient = models.CharField(null=False, db_index=True)
    subject = models.CharField()
    html_body = models.CharField()
    text_body = models.CharField()
    is_scheduled = models.BooleanField(default=False)
    scheduled_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "single_mails"
        ordering = ["created_at"]

    def __str__(self):
        return self.sender

    def __repr__(self):
        return self.sender
