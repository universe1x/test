from django.urls import path
from .views import create_application, application_detail



urlpatterns = [
    path('create/<int:owner_id>/', create_application, name='create_application'),
    path('my-applications/', application_detail, name='application_detail'),
]