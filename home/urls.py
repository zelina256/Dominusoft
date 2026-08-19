from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('rreth-nesh/', views.rrethnesh, name="rrethnesh"),
    path('kerkimi/', views.searchvenues, name="searchvenues"),
    path('abonohu/', views.subscribe, name="subscribe"),
    path('politikat_privatesi/', views.policy, name="policy"),
    path('termat_dhe_kushtet/', views.terms, name="terms"),
]
