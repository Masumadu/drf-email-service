from core.repository import SqlBaseRepository

from .models import MailAccountModel


class MailAccountRepository(SqlBaseRepository):
    model = MailAccountModel
    object_name = "mail_account"
