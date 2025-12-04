from django.urls import path
from .views import home

# urlspatterns = [
# path('', home, name='home')

# ]

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
