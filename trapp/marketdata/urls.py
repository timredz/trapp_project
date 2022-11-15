from django.urls import path
from . import views

app_name = 'marketdata'

urlpatterns = [
    path('', views.index),
    path('marketdata/', views.marketdata, name='index'),
    path('instruments', views.get_instruments),
    path('trade/<slug:ticker>', views.trade),
    path('candle/<slug:ticker>', views.get_candle_by_ticker),
    path('balance', views.show_balance),

    path('register_customer', views.register_customer),
    path('get_balance', views.get_balance),
    path('submit_order', views.submit_order),
]
