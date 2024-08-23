import uuid

import pinject
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from app.account.repository import MailAccountRepository
from app.delivery.repository import MailDeliveryRepository
from app.template.controller import MailTemplateController
from app.template.repository import MailTemplateRepository
from core.utils import api_responses

from .controller import SingleMailController
from .repository import SingleMailRepository
from .serializer import (
    PaginatedSingleMailSerializer,
    QuerySingleMailSerializer,
    SendSingleMailSerializer,
    SendSingleMailTemplateSerializer,
    SingleMailResponseSerializer,
    SingleMailSerializer,
)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        SingleMailController,
        SingleMailRepository,
        MailAccountRepository,
        MailDeliveryRepository,
        MailTemplateController,
        MailTemplateRepository,
    ],
)
single_mail_controller: SingleMailController = obj_graph.provide(SingleMailController)
api_doc_tag = ["SingleMail"]


@extend_schema(
    responses=api_responses(
        status_codes=[200, 401], schema=PaginatedSingleMailSerializer
    ),
    tags=api_doc_tag,
    parameters=[QuerySingleMailSerializer],
)
@api_view(http_method_names=["GET"])
def view_all_mails(request: Request):
    return single_mail_controller.view_all_mails(request)


@extend_schema(
    request=SendSingleMailSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=SingleMailResponseSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
def send_mail(request: Request):
    serializer = single_mail_controller.send_mail(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    request=SendSingleMailTemplateSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=SingleMailSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
def send_mail_with_template(request: Request):
    serializer = single_mail_controller.send_mail_with_template(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    responses=api_responses(status_codes=[200, 401, 404], schema=SingleMailSerializer),
    tags=api_doc_tag,
)
@api_view(http_method_names=["GET"])
def get_mail(request: Request, mail_id: uuid.UUID):
    serializer = single_mail_controller.get_mail(str(mail_id))
    return Response(data=serializer.data, status=200)


@extend_schema(
    responses=api_responses(status_codes=[204, 401, 404], schema=None),
    tags=api_doc_tag,
)
@api_view(http_method_names=["DELETE"])
def delete_mail(request: Request, mail_id: uuid.UUID):
    result = single_mail_controller.delete_mail(str(mail_id))
    return Response(data=result, status=204)
