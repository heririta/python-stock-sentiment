import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
import streamlit as st
from gnews import GNews
from datetime import datetime as DT
from dateutil import tz

def get_ticker_data(ticker_symbol, data_period, data_interval):
    ticker_data = yf.download(tickers=ticker_symbol,
                              period=data_period, interval=data_interval)

    if len(ticker_data) == 0:
        st.write("tidak ditemukan data emiten")
    else:
        ticker_data.index = ticker_data.index.strftime("%d-%m-%Y %H:%M")
    return ticker_data


def plot_candle_chart(ticker_data):
    candle_fig = go.Figure()
    candle_fig.add_trace(
        go.Candlestick(x=ticker_data.index,
                       open=ticker_data['Open'],
                       close=ticker_data['Close'],
                       low=ticker_data['Low'],
                       high=ticker_data['High'],
                       name='Market Data'
                       )
    )
    candle_fig.update_layout(
        height=600
    )
    st.write(candle_fig)

def search_key(word):
    google_news = GNews(language='id', country='ID', period='1y', max_results=100,
                        exclude_websites=None)

    # st.write(google_news)
    # st.write(type(google_news))
    news = google_news.get_news(word)
    # st.write(news)
    # st.write(type(news))
    return news

def date_convert(gmt_date):
    # st.write("Date in GMT: {0}".format(gmt_date) ")
    # Hardcode from and to time zones
    from_zone = tz.gettz('GMT')
    to_zone = tz.gettz('US/Eastern')
    # gmt = datetime.gmtnow()
    gmt = DT.strptime(gmt_date, '%a, %d %b %Y %H:%M:%S GMT')
    # Tell the datetime object that it's in GMT time zone
    gmt = gmt.replace(tzinfo=from_zone)
    gmt = gmt.strftime('%Y-%m-%d')
    # Convert time zone
    # eastern_time = str(gmt.astimezone(to_zone))
    # Check if its EST or EDT
    # if eastern_time[-6:] == "-05:00":
    #     st.write("Date in US/Eastern: " +eastern_time.replace("-05:00"," EST")")
    # elif eastern_time[-6:] == "-04:00":
    #     st.write("Date in US/Eastern: " +eastern_time.replace("-04:00"," EDT")")
    return gmt
    
    
# https://neptune.ai/blog/sentiment-analysis-python-textblob-vs-vader-vs-flair