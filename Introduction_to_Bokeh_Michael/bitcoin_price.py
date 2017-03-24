import requests
import pandas as pd
from datetime import datetime
import pytz


def bitcoin_price_history(start, end):
    url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
    date_range = "?start={}&end={}"
    request_url = url + date_range.format(start, end)
    response = requests.get(request_url)
    dt = response.json()
    dt = pd.DataFrame([{'date': datetime.strptime(d[0], '%Y-%m-%d'),
                        'price': float(d[1])} for d in dt['bpi'].items()])
    return dt

def bitcoin_current_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    dt = response.json()
    update = datetime.strptime(dt['time']['updated'], '%b %d, %Y %H:%M:%S %Z')
    local_dt = update.replace(tzinfo=pytz.utc).astimezone(tz=None).replace(tzinfo=None)
    price = round(float(dt['bpi']['USD']['rate'].replace(',', '')), 2)
    return local_dt, price


if __name__ == "__main__":
    pass
    print(bitcoin_price_history('2016-03-15', '2017-03-18'))
    # print(bitcoin_current_price())
