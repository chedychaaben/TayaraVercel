from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAnnonces),
    path('add/', views.addAnnonce)
]