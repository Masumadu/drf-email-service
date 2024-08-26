from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_mails, name="view_all_mails"),
    path("send/", views.send_mail, name="send_mail"),
    path("send/template/", views.send_mail_with_template, name="send_template_mail"),
    path("<uuid:mail_id>/detail/", views.get_mail, name="get_mail"),
    path("<uuid:mail_id>/delete/", views.delete_mail, name="delete_mail"),
]
