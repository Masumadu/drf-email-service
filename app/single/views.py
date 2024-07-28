import pinject
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.account.repository import MailAccountRepository
from app.delivery.repository import MailDeliveryRepository
from app.template.controller import MailTemplateController
from app.template.repository import (
    MailTemplateRepository,
    ObjectStorageLogRepository,
)
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
        ObjectStorageLogRepository,
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
    auth=[],
)
@api_view(http_method_names=["GET"])
def view_all_mails(request):
    return single_mail_controller.view_all_mails(request)


@extend_schema(
    request=SendSingleMailSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=SingleMailResponseSerializer
    ),
    auth=[],
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
def send_mail(request):
    serializer = single_mail_controller.send_mail(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    request=SendSingleMailTemplateSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=SingleMailSerializer
    ),
    tags=api_doc_tag,
    auth=[],
)
@api_view(http_method_names=["POST"])
def send_mail_with_template(request):
    serializer = single_mail_controller.send_mail_with_template(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    responses=api_responses(status_codes=[200, 401, 404], schema=SingleMailSerializer),
    tags=api_doc_tag,
    auth=[],
)
@api_view(http_method_names=["GET"])
def get_mail(request, mail_id):
    serializer = single_mail_controller.get_mail(mail_id)
    return Response(data=serializer.data, status=200)


@extend_schema(
    responses=api_responses(status_codes=[204, 401, 404], schema=None),
    tags=api_doc_tag,
    auth=[],
)
@api_view(http_method_names=["DELETE"])
def delete_mail(request, mail_id):
    result = single_mail_controller.delete_mail(mail_id)
    return Response(data=result, status=204)
