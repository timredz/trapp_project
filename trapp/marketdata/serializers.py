from rest_framework import serializers
from .models import Instruments, Orderbook, Candles10min, Balance, MyTrades, MyOrders


class InstrumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instruments
        fields = ('__all__')


class OrderbookSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = Orderbook
        fields = ('__all__')


class CandleSerializer(serializers.ModelSerializer):
    pr_open = serializers.FloatField()
    pr_high = serializers.FloatField()
    pr_low = serializers.FloatField()
    pr_close = serializers.FloatField()

    class Meta:
        model = Candles10min
        fields = ('__all__')


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ('currency', 'quantity')


class MyTradesSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = MyTrades
        fields = ('tradeID', 'ticker', 'buysell', 'price', 'quantity', 'tradetime')


class MyOrdersSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = MyOrders
        fields = ('orderID', 'ticker', 'buysell', 'price', 'quantity', 'balance', 'entrytime')
