# Generated by Django 5.1 on 2024-08-23 12:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("template", "0006_alter_mailtemplatemodel_object_storage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailtemplatemodel",
            name="object_storage",
        ),
        migrations.RemoveField(
            model_name="mailtemplatemodel",
            name="file_sys_path",
        ),
        migrations.DeleteModel(
            name="ObjectStorageLogModel",
        ),
    ]
