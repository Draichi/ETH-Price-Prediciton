import requests
import datetime

TOKEN_NAME_TO_ID = {
    'SNX': '2586',
    'BTC': '1',
    'ETH': '1027',
    'YFI': '5864',
    'CRV': '6538',
    'AAVE': '7278',
    'UNI': '7083',
    'sXAU': '6191',
    'sXAG': '5863',
    'sDEFI': '5862',
    'iBTC': '6200',
    'iETH': '6188',
}


def get_datasets(asset_name: str, days: int = 90) -> object:
    """Get datasets from Coinmarketcap API

    Args:
        asset_name (str): Ex.: 'BTC'

    Returns:
        object: Pandas Dataframe including Price, MarketCap, Volume
    """
    asset_id = TOKEN_NAME_TO_ID[asset_name]
    url = get_endpoint(asset_id=asset_id, days=days)
    print('> Fetching {}'.format(asset_name))
    res = requests.get(url).json()
    data: list = res['data']
    print(data)
    quit()
    temp_dataset = {
        'ds': [],
        'y': []
    }
    for (timestamp, price_obj) in data.items():
        timestamp = timestamp.split('T')[0]
        price = price_obj['USD'][0]
        volume = price_obj['USD'][1]
        market_cap = price_obj['USD'][2]
        temp_dataset['ds'].append(timestamp)
        temp_dataset['y'].append(price_obj['USD'][0])


def gen_indicators(df: object) -> object:
    """Generate technical indicators

    Args:
        df (Pandas Dataframe): Dataframe including Price, MarketCap, Volume

    Returns:
        Pandas Dataframe: Dataframe including Indicators Columns
    """
    pass


def gen_label(df: object, days: int = 7) -> object:
    """Generate label column

    Args:
        df (Pandas Dataframe): Dataframe Price

    Returns:
        Pandas Dataframe: Dataframe including Price in the next x days
    """
    pass


def get_actual_epoch() -> int:
    """Get actual epoch timestamp

    Returns:
        int: Actual timestamp
    """
    return int(datetime.datetime.now().timestamp())


def get_endpoint(asset_id: int, days: int = 90) -> str:
    """Get dataset download endpoint

    Args:
        asset_id (int): Ex.: 1 (for BTC)

    Returns:
        str: URL
    """
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    time_end = str(int(end_date.timestamp()))
    time_start = str(int(start_date.timestamp()))
    # feb_11_timestamp = str(1518389909)

    url = 'https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?convert=USD&format=chart_crypto_details&id=' + \
        str(asset_id)+'&interval=1d&time_end=' + \
        time_end+'&time_start='+time_start
    return url


get_datasets('sDEFI', 15)
