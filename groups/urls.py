from django.urls import path, include
from .views import create_group, group_list

urlpatterns = [
    path('', group_list, name='group_list'),
    path('create/', create_group, name='create_group'),
]
