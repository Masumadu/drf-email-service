# Generated by Django 5.0.6 on 2024-07-14 15:33

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailAccountModel",
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
                (
                    "mail_address",
                    models.EmailField(db_index=True, max_length=254, unique=True),
                ),
                ("sender_name", models.CharField()),
                ("_password", models.CharField(db_column="password")),
                ("is_default", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "mail_accounts",
                "ordering": ["created_at"],
            },
        ),
    ]