# Generated by Django 5.0.6 on 2024-07-14 15:33

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailDeliveryModel",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.CharField(null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("updated_by", models.CharField(null=True)),
                ("deleted_at", models.DateTimeField(null=True)),
                ("deleted_by", models.CharField(null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("user_id", models.UUIDField(db_index=True)),
                ("single_mail_id", models.UUIDField(db_index=True, null=True)),
                ("bulk_mail_id", models.UUIDField(db_index=True, null=True)),
                ("provider", models.CharField()),
                ("status", models.CharField()),
                ("total_recipients", models.IntegerField()),
                ("comment", models.JSONField()),
            ],
            options={
                "db_table": "delivery_reports",
                "ordering": ["created_at"],
            },
        ),
    ]
