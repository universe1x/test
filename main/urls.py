from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.reg, name='reg'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
]