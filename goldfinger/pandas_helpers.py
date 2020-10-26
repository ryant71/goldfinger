
import pandas as pd
import metals_api

metals_dict = {
    'XAU': 'Gold',
    'XAG': 'Silver'
}

def redis_to_dataframe(metal_currency_key):
    """
    Parameter: The key in Redis.
               E.g. XAU-USD
    """

    currency = metal_currency_key.split('-')[1]
    metal = metal_currency_key.split('-')[0]

    df = metals_api.redis_to_dataframe(metal_currency_key)

    # convert usd pricing
    if currency == 'USD':
        df['DateValue'] = df.DateValue.apply(lambda x: 1/x)

    # Add description columns
    df.insert(1, 'Stock', metals_dict[metal], allow_duplicates=True)
    df.insert(2, 'Currency', currency, allow_duplicates=True)

    # Add daily change column. As easy as.
    df['Change'] = df['DateValue'].diff()

    # Make Date column a datetime series
    df['Date'] = pd.to_datetime(df['Date'])

    # Make the Date column the index
    df.set_index('Date', inplace=True)

    return df


def concatenate_dataframes(frame_one, frame_two, ignore_index=False):
    return pd.concat([frame_one, frame_two], ignore_index)
