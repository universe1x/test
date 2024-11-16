from django.urls import path, include
from .views import create_group

urlpatterns = [
    path('create/', create_group, name='create_group'),
]
