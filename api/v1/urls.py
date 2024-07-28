from django.urls import include, path

urlpatterns = [
    path("single-mails/", include("app.single.urls")),
    path("bulk-mails/", include("app.bulk.urls")),
    path("accounts/", include("app.account.urls")),
    path("templates/", include("app.template.urls")),
]
