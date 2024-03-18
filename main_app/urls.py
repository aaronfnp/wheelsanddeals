from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('car_market/', views.car_market, name='car_market'),
    path('my_garage/', views.my_garage, name='my_garage'),
]