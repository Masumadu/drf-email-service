import uuid

from core.exceptions import AppException

from .repository import MailAccountRepository
from .serializer import (
    AddMailAccountSerializer,
    MailAccountSerializer,
    UpdateMailAccountSerializer,
)


class MailAccountController:
    def __init__(self, mail_account_repository: MailAccountRepository):
        self.mail_account_repository = mail_account_repository

    def view_all_accounts(self, request):
        paginator, result = self.mail_account_repository.index(request)
        serializer = MailAccountSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def add_account(self, request):
        serializer = AddMailAccountSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data["user_id"] = str(uuid.uuid4())
            mail_account = self.mail_account_repository.create(data)
            return MailAccountSerializer(mail_account)
        raise AppException.ValidationException(error_message=serializer.errors)

    def get_account(self, obj_id: str):
        return MailAccountSerializer(self.mail_account_repository.find_by_id(obj_id))

    def update_account(self, request, obj_id: str):
        serializer = UpdateMailAccountSerializer(data=request.data)
        if serializer.is_valid():
            mail_account = self.mail_account_repository.update_by_id(
                obj_id=obj_id, obj_data=serializer.validated_data
            )
            return MailAccountSerializer(mail_account)
        raise AppException.ValidationException(error_message=serializer.errors)

    def delete_account(self, obj_id: str):
        self.mail_account_repository.delete_by_id(obj_id)
        return None
