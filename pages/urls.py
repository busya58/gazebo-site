from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("besedki/", views.catalog, {"kind": "gazebo"}, name="gazebos"),
    path("volery/", views.catalog, {"kind": "enclosure"}, name="enclosures"),
    path(
        "zimnie-volery/",
        views.winter_enclosures,
        name="winter_enclosures",
    ),
   path("model/<str:slug>/", views.product_detail, name="product_detail"),
    path("nashi-proekty/", views.projects, name="projects"),
    path("zayavka/", views.application_create, name="application_create"),
    path("spasibo/", views.thanks, name="thanks"),
]