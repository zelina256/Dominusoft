from django.urls import path
from . import views

urlpatterns = [
    path("", views.services, name="services"),
    path('<str:services_slug>', views.service_detail, name="service_detail"),
]
