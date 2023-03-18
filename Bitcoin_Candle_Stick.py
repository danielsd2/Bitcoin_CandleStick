import pandas as pd
from pycoingecko import CoinGeckoAPI
import plotly.graph_objs as go
import plotly.offline as pyo

cg = CoinGeckoAPI()

# Using CoinGecko API to present the price of Bitcoin over the last 30 days.

# loading the data for bitcoin as usd currency
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

# creating a pandas DataFrame from the prices list obtained from the CoinGecko API.
# The DataFrame contains two columns: 'TimeStamp' and 'Price'
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])

# Changing the time stamp to be in as a date units
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

# Creating a candle stick to be presented. Using  the agg() method to apply multiple aggregations.
candlestick_data = data.groupby(data.Date.dt.date).agg({'Price': ['min', 'max', 'first', 'last']})

# Using plotly
fig = go.Figure(data=go.Candlestick(x=candlestick_data.index,
                                    open=candlestick_data['Price']['first'],
                                    high=candlestick_data['Price']['max'],
                                    low=candlestick_data['Price']['min'],
                                    close=candlestick_data['Price']['last']))
fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price( USD$ )', title="Bitcoin "
                                                                                                          "Candlestick Chart for last 30 days")

pyo.plot(fig, filename='bitcoin_candleStick.html')
