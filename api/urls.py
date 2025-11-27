from django.urls import path
from.views import home

urlspatterns = [
    path('', home, name='home')

]