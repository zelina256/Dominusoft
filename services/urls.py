from django.urls import path
from . import views

urlpatterns = [
    path("", views.services, name="services"),
    path('sherbim/', views.tech_services, name="tech_services"),
]
