from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('rreth_nesh/',views.about, name="about"),
    path('kerkimi/',views.searchvenues, name="searchvenues"),
    path('politikat_privatesi/',views.policy, name="policy"),
    path('termat_dhe_kushtet/',views.terms, name="terms"),
]