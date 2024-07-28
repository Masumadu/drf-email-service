from core.repository import SqlBaseRepository

from .models import MailTemplateModel, ObjectStorageLogModel


class MailTemplateRepository(SqlBaseRepository):
    """
    A repository class for handling operations related to mail template.
    This class extends `SqlBaseRepository` and specifies the model as `MailTemplateModel`
     with the object name 'mail_template'.
    """

    model = MailTemplateModel
    object_name = "mail_template"


class ObjectStorageLogRepository(SqlBaseRepository):
    """
    A repository class for handling operations related to mail template.
    This class extends `SqlBaseRepository` and specifies the model as
    `ObjectStorageLogModel` with the object name 'object_log'.
    """

    model = ObjectStorageLogModel
    object_name = "object_log"