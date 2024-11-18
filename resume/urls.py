from django.urls import path
from .views import create_resume, resume_detail



urlpatterns = [
    path('create/', create_resume, name='create_resume'),
    path('resume/<int:pk>/', resume_detail, name='resume_detail'),
]
