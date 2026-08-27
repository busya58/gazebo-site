from django.urls import path

from . import views

app_name = "cabinet"

urlpatterns = [
    path(
        "",
        views.dashboard_view,
        name="dashboard",
    ),
    path(
        "register/",
        views.register_view,
        name="register",
    ),
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "applications/create/",
        views.application_create_view,
        name="application_create",
    ),
    path(
        "applications/<int:pk>/",
        views.application_detail_view,
        name="application_detail",
    ),
    path(
    "review/create/",
    views.review_create,
    name="review_create",
    ),
]