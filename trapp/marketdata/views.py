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

from django.views.decorators.cache import cache_page

from .serializers import (
    MyOrdersSerializer, OrderbookSerializer, CandleSerializer, BalanceSerializer, MyTradesSerializer
)

CACHE_TTL = 60*5

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

fx_dict = {
	"USD000UTSTOM": {"name": "USD/RUB", "base": "RUB", "asset": "USD", "lot": 1000, "symbol": "$"},
	"EUR_RUB__TOM": {"name": "EUR/RUB", "base": "RUB", "asset": "EUR", "lot": 1000, "symbol": "€"},
	"CNYRUB_TOM": {"name": "CNY/RUB", "base": "RUB", "asset": "CNY", "lot": 1000, "symbol": "¥"},
	"USDCNY_TOM": {"name": "USD/CNY", "base": "CNY", "asset": "USD", "lot": 1000, "symbol": "$"},
	"KZTRUB_TOM": {"name": "KZT/RUB", "base": "RUB", "asset": "KZT", "lot": 1000, "symbol": "₸"},
	"HKDRUB_TOM": {"name": "HKD/RUB", "base": "RUB", "asset": "HKD", "lot": 1000, "symbol": "HK$"},
	"TRYRUB_TOM": {"name": "TRY/RUB", "base": "RUB", "asset": "TRY", "lot": 1000, "symbol": "₤"},
	"EURUSD000TOM": {"name": "EUR/USD", "base": "USD", "asset": "EUR", "lot": 1000, "symbol": "€"},
}

@cache_page(CACHE_TTL)
def index(request):
    template = 'index.html'
    return render(request, template)


def show_balance(request):
    template = 'balance.html'
    return render(request, template)


@api_view(['POST'])
def get_balance(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")
        result = Balance.objects.filter(customerID=customerID).values('currency', 'quantity')
        balance = {}
        for item in result:
            balance[item['currency']] = item['quantity']
        #serializer = BalanceSerializer(result, many=True)
        return Response(balance)




def trade(request, ticker):
    template = 'trade.html'
    pair = fx_dict[ticker]
    result = Candles10min.objects.filter(ticker=ticker).values('ticker', 'pr_close', 'valid_time')
    #collateral = Balance.objects.filter(ticker=ticker).values('ticker', 'pr_close', 'valid_time')
    result = result.reverse()[0]

    return render(request, template, {"ticker": ticker, "pair": pair, "last": result['pr_close']})



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
        name = request.data.get("name")
        phone = request.data.get("phone")
        email = request.data.get("email")
        reg_date = request.data.get("reg_date")
        amount = random.randrange(1, 20)

        #register customer
        customer = Customers(
            customerID=customerID,
            reg_date=reg_date,
            name=name,
            phone=phone,
            email=email
        )


        #create acc
        acc_rub = Balance(
            customerID=customerID,
            currency='RUB',
            quantity=50000*(5+amount),
            quantity_rub=50000*(5+amount)
        )

        acc_usd = Balance(
            customerID=customerID,
            currency='USD',
            quantity=0,
            quantity_rub=0
        )

        acc_eur = Balance(
            customerID=customerID,
            currency='EUR',
            quantity=0,
            quantity_rub=0
        )

        customer.save()
        acc_rub.save()
        acc_usd.save()
        acc_eur.save()

        return Response({"success":"true"})


@api_view(['POST'])
def submit_order(request):
    if request.method == 'POST':
        customerID = request.data.get("customerID")
        price = request.data.get("price")
        quantity = request.data.get("quantity")
        buysell = request.data.get("buysell")
        ticker = request.data.get("ticker")
        orderID = int(time.time())
        rest = quantity

        pair = fx_dict[ticker];

        ob = Orderbook.objects.filter(ticker=ticker.upper()).values('buysell', 'price', 'quantity')
        if buysell == 'B':
            if price==0:
                price = ob[9]['price']
        elif buysell == 'S':
            if price==0:
                price = ob[10]['price']

        if buysell == 'B':
            if price >= ob[9]['price']:
                rest = 0
        elif buysell == 'S':
            if price <= ob[10]['price']:
                rest = 0

        # transaction
        if buysell == 'B':
            if rest == 0:
                balance_base = Balance.objects.filter(customerID=customerID,currency=pair['base'])
                balance_asset = Balance.objects.filter(customerID=customerID,currency=pair['asset'])

                base_quantity = balance_base.values('quantity')[0]['quantity']
                asset_quantity = balance_asset.values('quantity')[0]['quantity']

                balance_base.update(quantity=base_quantity - price * fx_dict[ticker]['lot'] * quantity)
                balance_asset.update(quantity=asset_quantity + fx_dict[ticker]['lot'] * quantity)

        elif buysell == 'S':
            if rest == 0:
                balance_base = Balance.objects.filter(customerID=customerID, currency=pair['asset'])
                balance_asset = Balance.objects.filter(customerID=customerID, currency=pair['base'])

                base_quantity = balance_base.values('quantity')[0]['quantity']
                asset_quantity = balance_asset.values('quantity')[0]['quantity']

                balance_base.update(quantity=base_quantity - fx_dict[ticker]['lot'] * quantity)
                balance_asset.update(quantity=asset_quantity + price * fx_dict[ticker]['lot'] * quantity)




        order = MyOrders(
            customerID=customerID,
            orderID=orderID,
            ticker=ticker,
            price=price,
            quantity=quantity,
            buysell=buysell,
            balance=rest,
            value=int(price*quantity*fx_dict[ticker]['lot']),
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
