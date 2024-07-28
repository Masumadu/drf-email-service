from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_templates, name="view_all_templates"),
    path("upload/", views.add_template, name="add_template"),
    path(
        "<uuid:template_id>/placeholder/",
        views.add_template_placeholders,
        name="add_placeholders",
    ),
    path("<uuid:template_id>/detail/", views.get_template, name="get_template"),
    path("<uuid:template_id>/update/", views.update_template, name="update_template"),
    path("<uuid:template_id>/delete/", views.delete_template, name="delete_template"),
]
