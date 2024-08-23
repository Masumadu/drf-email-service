import os
import re
import uuid

from django.core.files.storage import default_storage
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string

from core.exceptions import AppException
from core.utils import (
    remove_none_fields,
    validate_file_size,
    validate_file_type,
)

from .repository import MailTemplateRepository
from .serializer import (
    AddMailTemplateSerializer,
    MailTemplateSerializer,
    PlaceHolderSerializer,
    UpdateMailTemplateSerializer,
)

TEMPLATE_DIR = "templates"


class MailTemplateController:
    template_directory = "templates"

    def __init__(self, mail_template_repository: MailTemplateRepository):
        self.mail_template_repository = mail_template_repository

    def view_all_templates(self, request):
        paginator, result = self.mail_template_repository.index(request)
        serializer = MailTemplateSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def add_template(self, request):
        serializer = AddMailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            file = serializer.validated_data.get("file")
            try:
                self.mail_template_repository.find(filter_param={"name": name})
                raise AppException.ResourceExistException(
                    error_message=f"template with name {name} already exists"
                )
            except AppException.NotFoundException:
                mail_template = self.mail_template_repository.create(
                    obj_data={
                        "user_id": request.user.get("preferred_username"),
                        "name": name,
                    }
                )
                self.upload_to_minio(mail_template, file)
                return MailTemplateSerializer(mail_template)
        raise AppException.ValidationException(error_message=serializer.errors)

    # noinspection PyMethodMayBeStatic
    def upload_to_minio(self, template, file: None):
        if file:
            validate_file_type(file=file, allowed_extensions=["html"])
            validate_file_size(file=file)
            template.file.save(file.name, file)
        return file

    def add_template_placeholder(self, request, obj_id: str):
        serializer = PlaceHolderSerializer(many=True, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            mail_template = self.mail_template_repository.update_by_id(
                obj_id=obj_id, obj_data={"placeholders": data}
            )
            return MailTemplateSerializer(mail_template)
        raise AppException.ValidationException(error_message=serializer.errors)

    def get_template(self, obj_id: str):
        return MailTemplateSerializer(self.mail_template_repository.find_by_id(obj_id))

    def update_template(self, request, obj_id: str):
        serializer = UpdateMailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            template = self.mail_template_repository.find_by_id(obj_id)
            self.upload_to_minio(template, data.get("file"))
            if template.file_system_id:
                default_storage.delete(
                    os.path.join(self.template_directory, template.file_system_id)
                )
                data["file_system_id"] = None
            mail_template = self.mail_template_repository.update_by_id(
                obj_id=obj_id, obj_data=data
            )
            return MailTemplateSerializer(mail_template)
        raise AppException.ValidationException(error_message=serializer.errors)

    def delete_mail(self, obj_id: str):
        self.mail_template_repository.delete_by_id(obj_id)
        return None

    def generate_message(self, query_template: dict, keywords: dict):
        try:
            template = self.mail_template_repository.find(
                remove_none_fields(query_template)
            )
            template_path = self.download_template(template=template)
            message = render_to_string(template_path, keywords)
            if placeholders := template.placeholders:
                for placeholder in placeholders:
                    if placeholder.get("is_sensitive"):
                        item = placeholder.get("key")
                        keywords[item] = re.sub(".", "*", str(keywords.get(item)))
            redacted_message = render_to_string(template_path, keywords)
            return message, redacted_message
        except TemplateDoesNotExist as exc:
            raise AppException.InternalServerException(
                error_message=f"TemplateError({exc})"
            ) from exc

    def presigned_put(self, template, file):
        upload_url = (
            template.file.storage.connection.meta.client.generate_presigned_url(
                "put_object",
                Params={"Bucket": template.file.storage.bucket_name, "Key": file.name},
            )
        )
        template.file.name = file.name
        template.save()
        return upload_url

    def download_template(self, template):
        file_id = template.file_system_id or str(uuid.uuid4())
        if not default_storage.exists(os.path.join(self.template_directory, file_id)):
            with template.file.storage.open(template.file.name, "rb") as file:
                default_storage.save(
                    os.path.join(self.template_directory, template.file.name), file
                )
                self.mail_template_repository.update_by_id(
                    obj_id=template.id, obj_data={"file_system_id": template.file.name}
                )
                return template.file.name
        return template.file_system_id
