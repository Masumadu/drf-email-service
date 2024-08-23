import uuid

import pinject
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from core.utils import api_responses

from .controller import MailAccountController
from .repository import MailAccountRepository
from .serializer import (
    AddMailAccountSerializer,
    MailAccountSerializer,
    PaginatedMailAccountSerializer,
    QueryMailAccountSerializer,
    UpdateMailAccountSerializer,
)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[MailAccountController, MailAccountRepository],
)
mail_account_controller: MailAccountController = obj_graph.provide(
    MailAccountController
)
api_doc_tag = ["MailAccount"]


@extend_schema(
    responses=api_responses(
        status_codes=[200, 401], schema=PaginatedMailAccountSerializer
    ),
    tags=api_doc_tag,
    parameters=[QueryMailAccountSerializer],
)
@api_view(http_method_names=["GET"])
def view_all_accounts(request: Request):
    return mail_account_controller.view_all_accounts(request)


@extend_schema(
    request=AddMailAccountSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=MailAccountSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["POST"])
def add_account(request: Request):
    serializer = mail_account_controller.add_account(request)
    return Response(data=serializer.data, status=201)


@extend_schema(
    request=MailAccountSerializer,
    responses=api_responses(
        status_codes=[201, 401, 409, 422], schema=MailAccountSerializer
    ),
    tags=api_doc_tag,
)
@api_view(http_method_names=["GET"])
def get_account(request: Request, account_id: uuid.UUID):
    serializer = mail_account_controller.get_account(str(account_id))
    return Response(data=serializer.data, status=200)


@extend_schema(
    request=UpdateMailAccountSerializer,
    responses=api_responses(status_codes=[200, 401, 404], schema=MailAccountSerializer),
    tags=api_doc_tag,
)
@api_view(http_method_names=["PATCH"])
def update_account(request: Request, account_id: uuid.UUID):
    serializer = mail_account_controller.update_account(request, str(account_id))
    return Response(data=serializer.data, status=200)


@extend_schema(
    responses=api_responses(status_codes=[204, 401, 404], schema=None),
    tags=api_doc_tag,
)
@api_view(http_method_names=["DELETE"])
def delete_account(request: Request, account_id: uuid.UUID):
    result = mail_account_controller.delete_account(request, str(account_id))
    return Response(data=result, status=204)
