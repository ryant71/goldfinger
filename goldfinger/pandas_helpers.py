# -*- coding: utf-8 -*-

import os
import redis
import pandas as pd

metals_dict = {
    'XAU': 'Gold',
    'XAG': 'Silver'
}

running_in_docker= os.environ.get('RUNNING_IN_DOCKER', False)

if running_in_docker:
    r = redis.Redis(host='192.168.1.21')
else:
    r = redis.Redis(host='127.0.0.1')


def redis_to_dataframe(key):
    timeseries_data = r.hgetall(key)
    timeseries_data = {
        k.decode('utf-8'):float(v) for (k,v) in timeseries_data.items()
    }
    df = pd.DataFrame(timeseries_data.items(), columns=['Date', 'DateValue'])
    pd.to_datetime(df['Date'])
    return df


def get_mangled_dataframe(metal_currency_key):
    """
    Parameter: The key in Redis.
               E.g. XAU-USD
    """

    currency = metal_currency_key.split('-')[1]
    metal = metal_currency_key.split('-')[0]

    df = redis_to_dataframe(metal_currency_key)

    # convert usd pricing
    if currency == 'USD':
        df['DateValue'] = df.DateValue.apply(lambda x: 1/x)

    # Add description columns
    df.insert(1, 'Stock', metals_dict[metal], allow_duplicates=True)
    df.insert(2, 'Currency', currency, allow_duplicates=True)
    df.insert(3, 'Stock-Currency', metals_dict[metal]+'-'+currency, allow_duplicates=True)

    # Add daily change column. As easy as.
    df['Change'] = df['DateValue'].diff()

    # Make Date column a datetime series
    df['Date'] = pd.to_datetime(df['Date'])

    # Make the Date column the index
    df.set_index('Date', inplace=True)

    return df


def concatenate_dataframes(args, ignore_index=False):
    return pd.concat(args, ignore_index)
