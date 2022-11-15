import time
import random
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .workers import instruments_data, candle_and_ob
from .models import Instruments, Orderbook, Candles10min, Candles1min, Customers, Balance, MyOrders

from .serializers import (
    InstrumentsSerializer, OrderbookSerializer, CandleSerializer, BalanceSerializer
)



def index(request):
    template = 'index.html'
    return render(request, template)


# any output on page
def marketdata(request):
    return HttpResponse('Any text')


def trade(request, ticker):
    template = 'trade.html'
    return render(request, template, {"ticker": ticker})


def show_balance(request):
    template = 'balance.html'
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

        order = MyOrders(
            customerID=customerID,
            orderID=int(time.time()),
            price=price,
            quantity=quantity,
            buysell=buysell,
            balance=quantity,
            value=int(price*quantity*1000),
            entrytime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        order.save()

        return Response({"order_placed":"true"})
