from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_accounts, name="view_all_accounts"),
    path("add/", views.add_account, name="add_account"),
    path("<uuid:account_id>/detail/", views.get_account, name="get_account"),
    path("<uuid:account_id>/update/", views.update_account, name="update_account"),
    path("<uuid:account_id>/delete/", views.delete_account, name="delete_account"),
]
