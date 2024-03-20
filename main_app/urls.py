from django.urls import path
from . import views
from .views import profile, ChangePasswordView
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
# from users.views import ChangePasswordView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('car_market/', views.car_market, name='car_market'),
    path('my_garage/', views.my_garage, name='my_garage'),
    path('cars/<int:car_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('my_garage/createreview/', views.ReviewCreate.as_view(), name='reviews_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)