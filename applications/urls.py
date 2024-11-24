from django.urls import path
from .views import create_application



urlpatterns = [
    path('create/', create_application, name='create_application'),
]