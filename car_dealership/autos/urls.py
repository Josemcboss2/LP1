from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('articles/', views.articles, name='articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('car_inquiry/', views.car_inquiry, name='car_inquiry'),
    path('articles/<int:article_id>/comment/', views.article_comment, name='article_comment'), 
    path('subscribe/', views.subscribe, name='subscribe'),
    path('register/', views.register, name='register'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
