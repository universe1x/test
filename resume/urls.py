from django.urls import path
from .views import create_resume, resume_detail, edit_resume



urlpatterns = [
    path('create/', create_resume, name='create_resume'),
    path('<int:pk>/', resume_detail, name='resume_detail'),
    path('<int:pk>/edit/', edit_resume, name='edit_resume'),
]
