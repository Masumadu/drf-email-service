import json
import mimetypes
import os
import uuid
from decimal import Decimal
from typing import Any, List

from django.conf import settings
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    OpenApiTypes,
)
from rest_framework.pagination import PageNumberPagination

from core.exceptions import AppException, exception_message


def api_requests(
    schema: Any, is_form_urlencoded: bool = False, is_multipart_form: bool = False
):
    if is_form_urlencoded:
        return {"application/x-www-form-urlencoded": schema}
    elif is_multipart_form:
        return {"multipart/form-data": schema}
    else:
        return {"application/json": schema}


def api_responses(status_codes: list, schema: Any):
    responses = {}
    over_all_exceptions = {
        400: OpenApiResponse(
            description="exception caused by invalid client requests",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.BadRequestException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.BadRequestException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        401: OpenApiResponse(
            description="exception caused by unauthenticated client requests",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.UnauthorizedException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.UnauthorizedException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        403: OpenApiResponse(
            description="exception caused by limited client permissions",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.PermissionException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.UnauthorizedException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        404: OpenApiResponse(
            description="exception caused by resource nonexistence on server",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.NotFoundException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.NotFoundException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        409: OpenApiResponse(
            description="exception caused by resource duplication on server",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.ResourceExistException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.ResourceExistException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        422: OpenApiResponse(
            description="exception caused by invalid client request data",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.ValidationException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.ValidationException.__name__,
                        message={"email": ["Enter a valid email address."]},
                    ),
                ),
            ],
        ),
        500: OpenApiResponse(
            description="exception caused by servers inability to process client request",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.InternalServerException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.InternalServerException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
        503: OpenApiResponse(
            description="exception caused by servers inability to access third party services",
            response=OpenApiTypes.OBJECT,
            examples=[
                OpenApiExample(
                    f"{AppException.ServiceUnavailableException.__name__} Response",
                    value=exception_message(
                        error_type=AppException.ServiceUnavailableException.__name__,
                        message="error message",
                    ),
                ),
            ],
        ),
    }
    for code in status_codes:
        if not over_all_exceptions.get(code):
            responses[code] = OpenApiResponse(
                description="successful response", response=schema
            )
        else:
            responses[code] = over_all_exceptions.get(code)
    return responses


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100


def validate_file_type(file, allowed_extensions: List[str] = None):
    allowed_extensions = allowed_extensions or ["html"]
    split_file_name = file.name.split(".")
    name, extension = split_file_name[:-1], split_file_name[-1]
    name = "".join(name).replace(" ", "_")
    if not extension:
        # reminder: use the content_type to determine the file extension
        guessed_extension = mimetypes.guess_extension(file.content_type)
        extension = guessed_extension[1:] if guessed_extension else None
    if extension not in allowed_extensions:
        raise AppException.BadRequestException(error_message="file type not allowed")
    return name, extension, file.content_type


def validate_file_size(file, allowed_size_in_mb: int = 5):
    if file.size > 1024 * 1024 * allowed_size_in_mb:
        raise AppException.BadRequestException(error_message="file too large")
    return allowed_size_in_mb


def create_directory(directory: str):
    # reminder: create the upload directory if it doesn't exist
    dir_path = os.path.join(settings.MEDIA_ROOT, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def file_path(directory: str, file_id: str):
    dir_path = create_directory(f"{directory}")
    return f"{dir_path}/{file_id}"


def save_file(path: str, file):
    with open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path


def delete_file(directory: str, file_id: str):
    file = f"{directory}/{file_id}"
    if os.path.exists(file):
        os.remove(file)
    return None


class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (Decimal, uuid.UUID)):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def remove_none_fields(data: dict):
    return {key: value for key, value in data.items() if value not in ["", None]}
