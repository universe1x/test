from django.urls import path, include
from .views import create_group, group_list, group_detail, edit_group, group_view

urlpatterns = [
    path('', group_list, name='group_list'),
    path('create/', create_group, name='create_group'),
    path('my-group/', group_detail, name='group_detail'),
    path('my-group/edit/', edit_group, name='edit_group'),
    path("<int:pk>", group_view, name='group_view'),

]
