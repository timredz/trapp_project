from django.http import HttpResponse
from django.shortcuts import render

import datetime

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .workers import instruments_data, candle_and_ob
from .models import Instruments, Orderbook, Candles10min, Candles1min

from .serializers import (
    InstrumentsSerializer, OrderbookSerializer, CandleSerializer
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
