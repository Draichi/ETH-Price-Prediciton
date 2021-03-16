#! ./venv/bin/activate

import requests
from ta.momentum import KAMAIndicator
import pandas as pd


def get_datasets(asset_name: str, currency: str, days: int, interval: str) -> pd.DataFrame:
    """Get prices, market_caps and total_volumes for a given asset

    Args:
        asset_name (str): Ex.: bitcoin
        currency (str): Defaults to 'USD'.
        days (int): Defaults to 2.
        interval (str): Defaults to 'daily'.

    Returns:
        Pandas DataFrame: Containing ds(timestamp), prices, total_volumes, market_caps
    """
    url = get_endpoint(asset_name=asset_name,
                       currency=currency, days=days, interval=interval)
    print('> Fetching {}'.format(asset_name))
    res: list('prices', 'total_volumes',
              'market_caps') = requests.get(url).json()
    temp_dataset = {
        'date': [],
        f'{asset_name}-prices': [],
        f'{asset_name}-total_volumes': [],
        f'{asset_name}-market_caps': []
    }
    timestamp_processed = False
    for indicator in res:
        indicator_list = res[indicator]
        for item in indicator_list:
            if not timestamp_processed:
                timestamp = item[0]
                temp_dataset['date'].append(timestamp)
            indicator_item = item[1]
            temp_dataset[f'{asset_name}-{indicator}'].append(indicator_item)
        timestamp_processed = True
    df = pd.DataFrame(temp_dataset)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)

    return df


def gen_features(df: pd.DataFrame, asset_name: str) -> pd.DataFrame:
    """Generate technical indicators

    Args:
        df (Pandas Dataframe): Dataframe including Price, MarketCap, Volume

    Returns:
        Pandas Dataframe: Dataframe including Indicators Columns
    """
    kama_indicator = KAMAIndicator(df[f'{asset_name}-prices'], window=2)
    df[f'{asset_name}-kama'] = kama_indicator.kama()
    df.dropna(inplace=True)
    return df


def gen_label(df: object, days: int = 7) -> object:
    """Generate label column

    Args:
        df (Pandas Dataframe): Dataframe Price

    Returns:
        Pandas Dataframe: Dataframe including Price in the next x days
    """
    pass


def get_endpoint(asset_name: str, currency: str, days: int, interval: str) -> str:
    url = 'https://api.coingecko.com/api/v3/coins/' + asset_name + \
          '/market_chart?vs_currency=' + currency + \
          '&days=' + str(days) + \
          '&interval=' + interval
    return url


def gen_df(asset_name: str, currency: str = 'USD', days: int = 2, interval: str = 'daily'):
    """Generate DataFrame

    Args:
        asset_name (str): Ex: bitcoin
        currency (str, optional): Ex: USD. Defaults to 'USD'.
        days (int, optional): Ex: 30. Defaults to 2.
        interval (str, optional): Ex: hourly. Defaults to 'daily'.

    Returns:
        Pandas DataFrame: Dataframe containing f'{asset_name}-prices', ..., f'{asset_name}-kama', ...
    """
    df = get_datasets(asset_name=asset_name, currency=currency,
                      days=days, interval=interval)
    df_features = gen_features(df=df, asset_name=asset_name)

    return df_features
