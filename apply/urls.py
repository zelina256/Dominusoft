from django.urls import path
from . import views

urlpatterns = [
    path('biznes', views.business, name="business"),
    path('karriera', views.career, name="career"),
    path('kursant', views.student, name="student"),
    path('kontakt', views.contact, name="contact"),
]