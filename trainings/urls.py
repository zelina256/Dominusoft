from django.urls import path
from . import views

urlpatterns = [
    path('', views.training_category, name="training_category"),
    path('<str:slug_training>', views.trainings, name="trainings"),
    path('<str:slug_training>/<str:kurrikula_slug>', views.curricula, name="curricula"),
]