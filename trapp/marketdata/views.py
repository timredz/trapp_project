import time
import random
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .workers import instruments_data, candle_and_ob, positions
from .models import Instruments, Orderbook, Candles10min, Candles1min, Customers, Balance, MyOrders, MyTrades
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from .serializers import (
    MyOrdersSerializer, OrderbookSerializer, CandleSerializer, BalanceSerializer, MyTradesSerializer
)

ticker_names = {
	"USD000UTSTOM": "USD/RUB",
	"EUR_RUB__TOM": "EUR/RUB",
	"CNYRUB_TOM": "CNY/RUB",
	"USDCNY_TOM": "USD/CNY",
	"KZTRUB_TOM": "KZT/RUB",
	"HKDRUB_TOM": "HKD/TOM",
	"TRYRUB_TOM": "TRY/RUB",
	"EURUSD000TOM": "EUR/USD"
}

@login_required
def index(request):
    template = 'index.html'
    return render(request, template)


# any output on page
def marketdata(request):
    send_mail('subj', 'message', 'fxworldteam@yandex.ru', ['tredzhepov@gmail.com'], fail_silently=False)
    return HttpResponse('Any text')


def trade(request, ticker):
    template = 'trade.html'
    pair = ticker_names[ticker]
    result = Candles10min.objects.filter(ticker=ticker).values('ticker', 'pr_close', 'valid_time')
    result = result.reverse()[0]

    return render(request, template, {"ticker": ticker, "pair": pair, "last": result['pr_close']})


def show_balance(request):
    template = 'balance.html'
    return render(request, template)


def ot(request):
    template = 'orders_trades.html'
    return render(request, template)


@api_view(['GET'])
def get_instruments(request):
    if request.method == 'GET':
        result = Candles1min.objects.all().values('ticker', 'pr_close', 'valid_time')
        result = instruments_data.get_instruments(result)
        return Response(result)


@api_view(['GET'])
def get_candle_by_ticker(request, ticker):
    if request.method == 'GET':
        candle = Candles10min.objects.filter(ticker=ticker.upper()).values('ticker', 'pr_open', 'pr_low', 'pr_high', 'pr_close', 'volume', 'valid_time').order_by('valid_time')
        ob = Orderbook.objects.filter(ticker=ticker.upper()).values('buysell', 'price', 'quantity')
        result = candle_and_ob.get_candle_ob(candle, ob)
        return Response(result)


@api_view(['POST'])
def register_customer(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")
        reg_date = request.data.get("reg_date")
        amount = random.randrange(1, 20)

        customer = Customers(customerID=customerID, reg_date=reg_date)
        customer_balance = Balance(
            customerID=customerID,
            cashin=50000*(5+amount),
            cashout=0,
            posvalue=0,
            total_value=50000*(5+amount)
        )

        customer.save()
        customer_balance.save()

        return Response({"success":"true"})


@api_view(['POST'])
def get_balance(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")

        result = Balance.objects.filter(customerID=customerID).values('total_value', 'posvalue')
        serializer = BalanceSerializer(result[0])
        return Response(serializer.data)


@api_view(['POST'])
def submit_order(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")
        price = request.data.get("price")
        quantity = request.data.get("quantity")
        buysell = request.data.get("buysell")
        ticker = request.data.get("ticker")
        orderID = int(time.time())

        order = MyOrders(
            customerID=customerID,
            orderID=orderID,
            ticker=ticker,
            price=price,
            quantity=quantity,
            buysell=buysell,
            balance=0,
            value=int(price*quantity*1000),
            entrytime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        order.save()

        time.sleep(2)
        trade = MyTrades(
            customerID=customerID,
            tradeID=(orderID % 10**5),
            orderID=orderID,
            ticker=ticker,
            price=price,
            quantity=quantity,
            buysell=buysell,
            value=int(price * quantity * 1000),
            tradetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        trade.save()

        return Response({"order_placed":"true"})


@api_view(['POST'])
def get_my_trades(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")

        result = MyTrades.objects.filter(customerID=customerID).values('tradeID', 'ticker', 'buysell', 'price', 'quantity', 'tradetime')
        serializer = MyTradesSerializer(result, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def get_my_orders(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")

        result = MyOrders.objects.filter(customerID=customerID).values('orderID', 'ticker', 'buysell', 'price', 'quantity', 'balance')
        serializer = MyOrdersSerializer(result, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def get_position(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")

        result = MyTrades.objects.filter(customerID=customerID).values('tradeID', 'ticker', 'buysell', 'price', 'quantity', 'tradetime')
        result = positions.get_position(result)
        return Response(result)
