from django.urls import path
from workers import views


urlpatterns = [
    path('', views.index),
    path('categories/', views.categories),
]
