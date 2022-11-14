from django.urls import path
from . import views

app_name = 'marketdata'

urlpatterns = [
    path('', views.index),
    path('marketdata/', views.marketdata, name='index'),
    path('instruments', views.get_instruments),
    path('trade/<slug:ticker>', views.trade),
    path('candle/<slug:ticker>', views.get_candle_by_ticker),
]
