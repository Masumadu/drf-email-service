from core.repository import SqlBaseRepository

from .models import SingleMailModel


class SingleMailRepository(SqlBaseRepository):
    model = SingleMailModel
    object_name = "email"
