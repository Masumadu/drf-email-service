import re
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from jinja2 import Environment as Jinja2Environment
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateError

from core.exceptions import AppException
from core.utils import (
    create_directory,
    file_path,
    save_file,
    validate_file_size,
    validate_file_type,
)

from .repository import (
    MailTemplateRepository,
    ObjectStorageLogRepository,
)
from .serializer import (
    AddMailTemplateSerializer,
    MailTemplateSerializer,
    PlaceHolderSerializer,
    UpdateMailTemplateSerializer,
)

TEMPLATE_DIR = "templates"


class MailTemplateController:
    def __init__(
        self,
        mail_template_repository: MailTemplateRepository,
        object_storage_log_repository: ObjectStorageLogRepository,
    ):
        self.mail_template_repository = mail_template_repository
        self.object_storage_log_repository = object_storage_log_repository
        self.download_directory = create_directory(TEMPLATE_DIR)
        # reminder: set TEMPLATE_DIR as the default directory for jinja2
        self.jinja2_environment = Jinja2Environment(
            loader=FileSystemLoader(self.download_directory)
        )

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
                file_id, upload = self.upload_template(
                    user_id=str(uuid.uuid4()), file=file
                )
                mail_template = self.mail_template_repository.create(
                    obj_data={
                        "user_id": str(uuid.uuid4()),
                        "name": name,
                        "file_sys_path": file_id,
                        "object_storage": upload,
                    }
                )
                return MailTemplateSerializer(mail_template)
        raise AppException.ValidationException(error_message=serializer.errors)

    def upload_template(self, user_id, file):
        file_name, ext, content_type = validate_file_type(
            file=file, allowed_extensions=["html", "jpg", "png"]
        )
        validate_file_size(file=file, allowed_size_in_mb=10)
        file_id = f"{uuid.uuid4()}_{file_name}.{ext}"
        object_storage_key = f"{TEMPLATE_DIR}/{user_id}/{file_id}"
        save_file(path=file_path(TEMPLATE_DIR, file_id), file=file)
        file_name = default_storage.save(object_storage_key, ContentFile(file.read()))
        file_url = default_storage.url(file_name)
        print("this is the file ", file_url, object_storage_key)
        upload = self.object_storage_log_repository.create(
            obj_data={
                "user_id": user_id,
                "bucket": "bucket",
                "key": object_storage_key,
                "name": file_name,
                "description": "user uploaded email template",
                "content_type": content_type,
                "created_by": user_id,
                "updated_by": user_id,
            }
        )
        return file_id, upload

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
            self.mail_template_repository.find_by_id(obj_id)
            if data.get("file"):
                file_id, upload = self.upload_template(
                    user_id=str(uuid.uuid4()), file=data.pop("file")
                )
                data["object_storage"] = upload
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
            mail_template = self.mail_template_repository.find(query_template)
            template = self.jinja2_environment.get_template(mail_template.file_sys_path)
            message = template.render(**keywords)
            if placeholders := mail_template.placeholders:
                for placeholder in placeholders:
                    if placeholder.get("is_sensitive"):
                        item = placeholder.get("key")
                        keywords[item] = re.sub(".", "*", str(keywords.get(item)))
            redacted_message = template.render(**keywords)
            return message, redacted_message
        except TemplateError as exc:
            raise AppException.InternalServerException(
                error_message=f"TemplateError({exc})"
            ) from exc
