"""
We return the values based in the base currency.
For example, for 1 USD the return is a number like 0.000634 for Gold (XAU).
To get the gold rate in USD: 1/0.000634= 1577.28 USD
"""

import boto3
import requests

API_URL = 'https://www.metals-api.com/api'

ssm = boto3.client('ssm')
access_key = ssm.get_parameter(Name='/goldfinger/api/key', WithDecryption=True)['Parameter']['Value']


def get_latest(currency='ZAR', *symbols):
    """
    "latest" endpoint - request the most recent exchange rate data

    https://www.metals-api.com/api/latest

      ? access_key = YOUR_ACCESS_KEY
      & base = USD
      & symbols = XAU,XAG
    """
    symbols = ','.join(symbols)
    uri = f'{API_URL}/latest?access_key={access_key}&base={currency}&symbols={symbols}'
    print(uri)
    ret = requests.get(uri)
    print(ret.status_code)
    print(ret.text)
    print(ret.json())

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


def get_timeseries():
    """
    "timeseries" endpoint - request exchange rates for a specific period of time

    https://www.metals-api.com/api/timeseries

      ? access_key = YOUR_ACCESS_KEY
      & start_date = YYYY-MM-DD
      & end_date = YYYY-MM-DD
      & base = USD
      & symbols = XAU,XAG
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

if __name__=="__main__":

    get_latest('ZAR', 'XAU', 'XAG')
