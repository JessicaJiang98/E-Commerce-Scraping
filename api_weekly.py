import requests
from bs4 import BeautifulSoup
import pandas as pd
#The API key is V5CVLX99TZCY17EN, number of requests that can be made each day is 500
#Get teh weekily stock price of the following four companies, LVMH, ZARA,Keurig,H&M
def get_api_weekly():
    symbols=['LVMUY','PPRUF','IDEXY','HNNMY']
    url = 'https://www.alphavantage.co/query?'
    param = {'function': 'TIME_SERIES_WEEKLY_ADJUSTED', 'symbol': symbols, 'datatype': 'json',
             'apikey': 'V5CVLX99TZCY17EN'}
    datalis={}
    #iterate through the tickers, and get their corresponding csv and dataframe one by one
    for symbol in symbols:
        api_response = requests.get(url, params=param)
        response_json=api_response.json()
        data = pd.DataFrame.from_dict(response_json['Weekly Adjusted Time Series'], orient='index').sort_index(axis=1)
        data = data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close',
                                    '5. adjusted close': 'AdjClose', '6. volume': 'Volume'})
        data = data[['Open', 'High', 'Low', 'Close', 'AdjClose', 'Volume']]
        datalis[symbol]=data
        data.to_csv(f'data/{symbol}_stock.csv',index=False,sep=',')
    return datalis