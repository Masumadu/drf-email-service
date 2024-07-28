from core.repository import SqlBaseRepository

from .models import MailDeliveryModel


class MailDeliveryRepository(SqlBaseRepository):
    """
    A repository class for handling operations related to a single mail delivery report.
    This class extends `SqlBaseRepository` and specifies the model as `MailDeliveryModel`
     with the object name 'delivery_report'.
    """

    model = MailDeliveryModel
    object_name = "delivery_report"
