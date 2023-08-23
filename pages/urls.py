from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('home', views.homePage.as_view(), name='home')
]