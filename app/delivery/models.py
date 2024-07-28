import uuid

from django.db import models

from app.bulk.models import BulkMailModel
from app.single.models import SingleMailModel
from core.models import BaseModel

# Create your models here.


class MailDeliveryModel(BaseModel):
    """
    A Django model representing a mail delivery report with fields like provider, status,
     and total recipients. The model `MailDeliveryModel` includes attributes for tracking
     delivery information and is associated with the database table 'delivery_reports'.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.UUIDField(null=False, db_index=True)
    single_mail = models.ForeignKey(
        to=SingleMailModel,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        related_name="delivery",
    )
    bulk_mail = models.ForeignKey(
        to=BulkMailModel,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        related_name="delivery",
    )
    provider = models.CharField(null=True)
    status = models.CharField(null=False)
    total_recipients = models.IntegerField(null=False, default=0)
    comment = models.JSONField(null=True)

    class Meta:
        db_table = "delivery_reports"
        ordering = ["created_at"]

    def __str__(self):
        return self.provider

    def __repr__(self):
        return self.provider
