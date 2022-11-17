from django.db import models


class Customers(models.Model):
    customerID = models.CharField(max_length=36)
    reg_date = models.BigIntegerField()


class Balance(models.Model):
    customerID = models.CharField(max_length=36)
    cashin = models.BigIntegerField()
    cashout = models.BigIntegerField()
    posvalue = models.BigIntegerField()
    total_value = models.BigIntegerField()


class MyOrders(models.Model):
    customerID = models.CharField(max_length=36)
    orderID = models.BigIntegerField(null=True)
    ticker = models.CharField(max_length=36)
    buysell = models.CharField(max_length=1)
    price = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    quantity = models.BigIntegerField()
    balance = models.BigIntegerField(null=True)
    value = models.BigIntegerField()
    entrytime = models.DateTimeField(null=True)
    expirytime = models.DateTimeField(null=True)


class MyTrades(models.Model):
    customerID = models.CharField(max_length=36)
    tradeID = models.BigIntegerField()
    orderID = models.BigIntegerField()
    ticker = models.CharField(max_length=36)
    buysell = models.CharField(max_length=1)
    price = models.DecimalField(max_digits=19, decimal_places=6)
    quantity = models.BigIntegerField()
    value = models.BigIntegerField()
    tradetime = models.DateTimeField()


class Instruments(models.Model):
    venue = models.CharField(max_length=36)
    ticker = models.CharField(max_length=36)
    pair = models.CharField(max_length=36)
    name_en = models.CharField(max_length=99)
    name_ru = models.CharField(max_length=99)
    lotsize = models.IntegerField(null=True)
    minstep = models.DecimalField(null=True, max_digits=19, decimal_places=6)


class Orderbook(models.Model):
    venue = models.CharField(max_length=36)
    ticker = models.CharField(max_length=36)
    buysell = models.CharField(max_length=1)
    price = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    quantity = models.BigIntegerField(null=True)
    decimals = models.IntegerField(null=True)
    valid_time = models.DateTimeField(null=True)


class Candles10min(models.Model):
    venue = models.CharField(max_length=36)
    ticker = models.CharField(max_length=36)
    pr_open = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_high = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_low = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_close = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    volume = models.BigIntegerField(null=True)
    turnover = models.BigIntegerField(null=True)
    valid_time = models.DateTimeField(null=True)


class Candles1min(models.Model):
    venue = models.CharField(max_length=36)
    ticker = models.CharField(max_length=36)
    pr_open = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_high = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_low = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    pr_close = models.DecimalField(null=True, max_digits=19, decimal_places=6)
    volume = models.BigIntegerField(null=True)
    turnover = models.BigIntegerField(null=True)
    valid_time = models.DateTimeField(null=True)

