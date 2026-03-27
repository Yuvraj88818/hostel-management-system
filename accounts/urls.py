from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_complaint, name='add_complaint'),
    path('view/', views.view_complaints, name='view_complaints'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('fee/', views.fee_status, name='fee'),
    path('register/', views.register, name='register'),
]