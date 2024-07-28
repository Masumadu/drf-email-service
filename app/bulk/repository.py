from core.repository import SqlBaseRepository

from .models import BulkMailModel


class BulkMailRepository(SqlBaseRepository):
    model = BulkMailModel
    object_name = "bulk_mail"
