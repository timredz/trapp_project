from django.urls import path
from . import views

app_name = 'marketdata'

urlpatterns = [
    path('', views.index),
    path('marketdata/', views.marketdata, name='index'),
]
