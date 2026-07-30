from django.urls import path
from . import views

urlpatterns = [
    path("", views.services, name="services"),
    # path('<str:slug>', views.tech_services, name="tech_services"),
]
