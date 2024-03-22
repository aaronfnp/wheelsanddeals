from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),
    path('garage/<int:user_id>', views.garage, name='garage'),
    path('garage/<int:user_id>/add_avatar/', views.add_avatar, name='add_avatar'),
    path('cars/<int:car_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('garage/<int:user_id>/createreview/', views.ReviewCreate.as_view(), name='reviews_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cars/categories/', views.car_list, name='car_list'), 
]