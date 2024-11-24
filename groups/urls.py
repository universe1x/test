from django.urls import path, include
from .views import create_group, group_list, group_detail

urlpatterns = [
    path('', group_list, name='group_list'),
    path('create/', create_group, name='create_group'),
    path('<int:pk>/', group_detail, name='group_detail'),
    
]
