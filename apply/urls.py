from django.urls import path
from . import views

urlpatterns = [
    path('', views.application, name="application"),
    path('biznes', views.legacy_business, name="business"),
    path('kursant', views.legacy_student, name="student"),
]