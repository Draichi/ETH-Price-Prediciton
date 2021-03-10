import requests
import ta
import pandas as pd


def get_datasets(asset_name: str, currency: str = 'USD', days: int = 2, interval: str = 'daily') -> pd.DataFrame:
    """Get prices, market_caps and total_volumes for a given asset

    Args:
        asset_name (str): Ex.: bitcoin
        currency (str, optional): Defaults to 'USD'.
        days (int, optional): Defaults to 2.
        interval (str, optional): Defaults to 'daily'.

    Returns:
        Pandas DataFrame: Containing ds(timestamp), prices, total_volumes, market_caps
    """
    url = get_endpoint(asset_name=asset_name,
                       currency=currency, days=days, interval=interval)
    print('> Fetching {}'.format(asset_name))
    res: list('prices', 'total_volumes',
              'market_caps') = requests.get(url).json()
    temp_dataset = {
        'ds': [],
        'prices': [],
        'total_volumes': [],
        'market_caps': []
    }
    timestamp_processed = False
    for indicator in res:
        indicator_list = res[indicator]
        for item in indicator_list:
            if not timestamp_processed:
                timestamp = item[0]
                temp_dataset['ds'].append(timestamp)
            indicator_item = item[1]
            temp_dataset[indicator].append(indicator_item)
        timestamp_processed = True
    df = pd.DataFrame(temp_dataset)
    df.set_index('ds', inplace=True)

    return df


def gen_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate technical indicators

    Args:
        df (Pandas Dataframe): Dataframe including Price, MarketCap, Volume

    Returns:
        Pandas Dataframe: Dataframe including Indicators Columns
    """
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


sdefi_df = get_datasets(asset_name='sdefi')

print(sdefi_df)

sdefi_features = gen_features(df=sdefi_df)
print(sdefi_features)
