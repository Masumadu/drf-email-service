# Generated by Django 5.0.6 on 2024-07-16 14:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bulk", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bulkmailmodel",
            name="_group_ids",
        ),
    ]
