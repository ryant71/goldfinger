# -*- coding: utf-8 -*-

"""
We return the values based in the base currency.
For example, for 1 USD the return is a number like 0.000634 for Gold (XAU).
To get the gold rate in USD: 1/0.000634= 1577.28 USD
"""

import math
import boto3
import redis
import requests
import pandas as pd

from datetime import date, datetime, timedelta
from helpers import get_today_date, get_days_ago_date, days_diff

MAX_DAYS = 5
API_URL = 'https://www.metals-api.com/api'


def get_access_key():
    ssm = boto3.client('ssm')
    return ssm.get_parameter(Name='/goldfinger/api/key', WithDecryption=True)['Parameter']['Value']


def get_latest(currency, *symbols):
    """
    "latest" endpoint - request the most recent exchange rate data

    https://www.metals-api.com/api/latest

      ? access_key = YOUR_ACCESS_KEY
      & base = USD
      & symbols = XAU,XAG
    """
    symbols = ','.join(symbols)
    uri = f'{API_URL}/latest?access_key={access_key}&base={currency}&symbols={symbols}'
    return requests.get(uri).json()


def get_timeseries(currency, start_date, end_date, symbol):
    """
    "timeseries" endpoint - request exchange rates for a specific period of time

    https://www.metals-api.com/api/timeseries

      ? access_key = YOUR_ACCESS_KEY
      & start_date = YYYY-MM-DD
      & end_date = YYYY-MM-DD
      & base = USD
      & symbols = XAU,XAG <-- can actually only be one symbol
    """
    uri = f'{API_URL}/timeseries?access_key={access_key}&start_date={start_date}&end_date={end_date}&base={currency}&symbols={symbol}'
    return requests.get(uri).json()


def get_historical():
    """
    "historical" endpoint - request historical rates for a specific day

    https://www.metals-api.com/api/YYYY-MM-DD

      ? access_key = YOUR_ACCESS_KEY
      & base = USD
      & symbols = XAU,XAG
    """
    pass


def get_convert():
    """
    "convert" endpoint - convert any amount from one currency to another
    using real-time exchange rates

    https://www.metals-api.com/api/convert

      ? access_key = YOUR_ACCESS_KEY
      & from = USD
      & to = EUR
      & amount = 25

    append an additional "date" parameter if you want to use
    historical rates for your conversion
      & date = YYYY-MM-DD
    """
    pass



def get_fluctuation():
    """
    "fluctuation" endpoint - request any currency's change parameters (margin
    and percentage), optionally between two specified dates

    https://www.metals-api.com/api/fluctuation

      ? access_key = YOUR_ACCESS_KEY
      & base = USD
      & symbols = XAU,XAG
      & type = weekly
    append an additional "date" parameter if you want to use
    historical rates for your conversion
      & start_date = YYYY-MM-DD
      & end_date = YYYY-MM-DD
    """
    pass


def timeseries_to_redis(currency, start_date_str, end_date_str, symbol):
    today = datetime.today()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    _days_diff = days_diff(start_date_str, end_date_str)
    loops = math.ceil(_days_diff / MAX_DAYS)
    rates = {}
    for loop in range(loops):
        start = start_date
        end = start_date + timedelta(MAX_DAYS)
        if end > today:
            end = today
        end_str =  end.strftime('%Y-%m-%d')
        start_str = start.strftime('%Y-%m-%d')
        start_date = end
        print(f'{start_str} to {end_str}', end='')
        # this does a hget each iteration, but I guess that's what a cache is for
        if not date_range_in_redis(start, currency, symbol):
            # redis does not have the keys in range
            ret = get_timeseries(currency, start_str, end_str, symbol)
        else:
            print('...already in redis')
            continue
        if not ret['success']:
            print(f'Bad response {ret}')
            break
        rates.update(ret['rates'])
        print(rates)
    # flatten dictionary
    rates_to_date = {
        k:v[symbol] for (k,v) in rates.items()
    }
    return {symbol: rates_to_date}

#end_date = get_today_date()
#start_date = get_days_ago_date(MAX_DAYS)


def date_range_in_redis(start_date, currency, symbol):
    key = f'{symbol}-{currency}'
    timeseries_data = r.hgetall(key)
    timeseries_data = {
        k.decode('utf-8'):float(v) for (k,v) in timeseries_data.items()
    }
    all_dates = set(timeseries_data.keys())
    range_dates =  set([(start_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(MAX_DAYS)])
    return range_dates.issubset(all_dates)


if __name__=="__main__":

    global r
    global access_key

    access_key = make_access_key()

    try:
        r = redis.Redis(host='192.168.1.21')
    except ConnectionRefusedError:
        r = redis.Redis(host='127.0.0.1')

    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

    for symbol in ['XAU', 'XAG']:
        for currency in ['ZAR', 'USD']:
            key = f'{symbol}-{currency}'
            series = timeseries_to_redis(currency, '2020-01-01', yesterday, symbol)
            print(series)
            if series:
                try:
                    r.hmset(key, series[symbol])
                    print(redis_to_dataframe(symbol))
                except redis.exceptions.DataError:
                    print('empty dictionary')
            else:
                print('Something went wrong')
