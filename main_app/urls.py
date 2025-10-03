from django.urls import path
from  . import views # views are similar to controllers

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]