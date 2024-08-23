from core.repository import SqlBaseRepository

from .models import MailTemplateModel


class MailTemplateRepository(SqlBaseRepository):
    """
    A repository class for handling operations related to mail template.
    This class extends `SqlBaseRepository` and specifies the model as `MailTemplateModel`
     with the object name 'mail_template'.
    """

    model = MailTemplateModel
    object_name = "mail_template"
