import pinject
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from core.utils import api_requests, api_responses

from .controller import MailTemplateController
from .repository import MailTemplateRepository
from .serializer import (
    MailTemplateSerializer,
    PaginatedMailTemplateSerializer,
    PlaceHolderSerializer,
    QueryMailTemplateSerializer,
)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        MailTemplateController,
        MailTemplateRepository,
    ],
)
mail_template_controller: MailTemplateController = obj_graph.provide(
    MailTemplateController
)
api_doc_tag = ["MailTemplate"]


@extend_schema(
    responses=api_responses(
        status_codes=[200, 401], schema=PaginatedMailTemplateSerializer
    ),
    tags=api_doc_tag,
    parameters=[QueryMailTemplateSerializer],
)
@api_view(http_method_names=["GET"])
def view_all_templates(request):
    return mail_template_controller.view_all_templates(request)


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "file": {"type": "string", "format": "binary"},
            },
            "required": ["name", "file"],
        }
    },
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=MailTemplateSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
@parser_classes([MultiPartParser, FormParser])
def add_template(request):
    serializer = mail_template_controller.add_template(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    request=api_requests(schema=PlaceHolderSerializer(many=True)),
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=MailTemplateSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
def add_template_placeholders(request, template_id):
    serializer = mail_template_controller.add_template_placeholder(request, template_id)
    return Response(data=serializer.data, status=201)


@extend_schema(
    responses=api_responses(
        status_codes=[200, 401, 404], schema=MailTemplateSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["GET"])
def get_template(request, template_id):
    serializer = mail_template_controller.get_template(template_id)
    return Response(data=serializer.data, status=200)


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "file": {"type": "string", "format": "binary"},
            },
        }
    },
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=MailTemplateSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["PATCH"])
def update_template(request, template_id):
    serializer = mail_template_controller.update_template(request, template_id)
    return Response(data=serializer.data, status=201)


@extend_schema(
    responses=api_responses(status_codes=[204, 401, 404], schema=None),
    tags=api_doc_tag,
)
@api_view(http_method_names=["DELETE"])
def delete_template(request, template_id):
    result = mail_template_controller.delete_mail(template_id)
    return Response(data=result, status=204)
