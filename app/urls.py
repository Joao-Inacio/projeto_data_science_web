from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('page/<int:page>/', views.home),
    path('countryFilter/', views.countryFilter),
    path('detalhes/<int:pk>/', views.detalhes),
]
