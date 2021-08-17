from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send/', views.sendView, name='send'),
    path('friend/', views.friendView, name='friend'),
]