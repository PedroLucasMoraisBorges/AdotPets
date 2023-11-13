from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:pk>/', views.chatRoom, name="chat"),
    path('send/', views.Send, name="send"),
    path('getMessages/<str:pk>/', views.getMessages, name="getMessages")
]
