from django.urls import path
from . import views

app_name = 'marketdata'

urlpatterns = [
    path('', views.index, name='index'),
    #path('marketdata/', views.marketdata),
    path('instruments', views.get_instruments),
    path('trade/<slug:ticker>', views.trade),
    path('candle/<slug:ticker>', views.get_candle_by_ticker),
    path('balance', views.show_balance),
    path('ot', views.ot),

    path('register_customer', views.register_customer),
    path('get_balance', views.get_balance),
    path('submit_order', views.submit_order),
    path('my_trades', views.get_my_trades),
    path('my_orders', views.get_my_orders),
    path('position', views.get_position),
]
