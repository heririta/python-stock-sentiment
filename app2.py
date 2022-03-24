import string
from threading import stack_size
from tkinter import HORIZONTAL
from gnews import GNews
import streamlit as st
import pandas as pd
import re  # impor modul regular expression
from newspaper import Config
from newspaper import Article
from textblob import TextBlob
from textblob import Word
from datetime import datetime as DT
from dateutil import tz
import yfinance as yf
import matplotlib.pyplot as plt
import numpy
import altair as alt
from streamlit_option_menu import option_menu
import plotly.graph_objs as go
import plotly.express as px
import util
from datetime import datetime


# https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sentimen Analisis",
                   page_icon=":art:", layout="wide")


selected = option_menu(
    menu_title=None,
    options=["Sentiment Analyst", "Market Indonesia", "Chart"],
    icons=["search", "bank2", "file-earmark-bar-graph-fill"],
    menu_icon="cast",
    default_index=1,
    orientation=HORIZONTAL,
)

if selected == "Sentiment Analyst":
    search = st.sidebar.text_input('Pencarian :', 'Ekonomi')
    # st.sidebar.write('The current is', search,)
    # st.sidebar.write(type(search))

    options = st.sidebar.multiselect(
        'Situs Pencarian  :',
        ['cnbcindonesia.com', 'cnnindonesia.com',
            'ekonomi.bisnis.com', 'money.kompas.com'],
        ['cnbcindonesia.com', 'cnnindonesia.com', 'ekonomi.bisnis.com', 'money.kompas.com'],)

    # st.sidebar.write('You selected:', options)
    # st.sidebar.write(type(options))

    # for x in options:
    #     st.write(x)
    #     st.write(type(x))

    # st.write('----------------------------------------------------------------')

    # for i in range(len(options)):
    #     word = "site:"+options[i]+" "+search
    #     st.write(word)
    #     st.write(type(options[i]))

    # st.write('----------------------------------------------------------------')

    def search_key(word):
        google_news = GNews(language='id', country='ID', period='1y', max_results=10,
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

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    hasilsearch = []
    # st.write(type(hasilsearch))

    # st.write('----------------------------------------------------------------')

    try:
        for i in range(len(options)):
            word = search+" site:"+options[i]
            # st.write(word)
            # st.dataframe(search_key(search))
            # st.write(len(search_key(word)))
            # st.write(type(search_key(search)))
            hasilsearch.extend(search_key(word))
    except Exception as e:
        st.write("")

    # st.write('----------------------------------------------------------------')

    hasilanalisis = []
    # st.write(len(hasilsearch))
    # st.write(type(hasilsearch))
    st.header("News - Sentimen Analisis")
    # st.write('----------------------------------------------------------------')
    for indonesia_news in hasilsearch:

        base_url = indonesia_news['url']

        article = Article(base_url, config=config)
        try:
            article.download()
            article.parse()
        except Exception as e:
            print("error download")

        published_date = indonesia_news["published date"]
        published_date2 = date_convert(published_date)
        # st.dataframe(hasilsearch)
        publish_date = article.publish_date
        st.write(published_date2)
        # st.write(type(published_date2))

        # st.write(publish_date)
        # st.write(type(publish_date))

        st.write(article.title)
        article_meta_data = article.meta_data
        article_summary = {value for (
            key, value) in article_meta_data.items() if key == 'description'}
        st.write(article_summary)
        try:
            news_properties = {}
            news_properties["title"] = article.title
            # news_properties["tanggal"] = publish_date.strftime('%Y-%m-%d')
            news_properties["tanggal"] = published_date2
            news_properties["isi_news"] = article_summary
            # st.write(type(article_summary))
        except Exception as e:
            print("error convert")
        # Tokenizing
        news_nilai = ' '.join(re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(\d+)", " ", str(article_summary)).split())
        # case folding
        news_nilai = news_nilai.lower()
        # Menghapus whitepace (karakter kosong)
        news_nilai = news_nilai.strip()
        # Menghapus tanda baca
        news_nilai = news_nilai.translate(
            str.maketrans('', '', string.punctuation))

        st.write(news_nilai)
        st.write(base_url)
        # st.write(news_properties["tanggal"])
        analysis = TextBlob(news_nilai)
        # st.write(analysis)
        try:
            analysis = analysis.translate(to="en")
        except Exception as e:
            print("error translate")
        # st.write(analysis)
        st.write(analysis.sentiment.polarity)

        if analysis.sentiment.polarity > 0.0:
            news_properties['sentimen'] = "Sentiment:: Positive :smiley:"
        elif analysis.sentiment.polarity == 0.0:
            news_properties['sentimen'] = "Sentiment:: Neutral 😐 "
        else:
            news_properties['sentimen'] = "Sentiment:: Negative :angry:"

        if analysis.sentiment.polarity > 0.0:
            news_properties['param'] = 1
        elif analysis.sentiment.polarity == 0.0:
            news_properties['param'] = 0
        else:
            news_properties['param'] = -1

        st.write(news_properties['sentimen'])

        hasilanalisis.append(news_properties)

    # st.write('----------------------------------------------------------------')

    news_positif = [t for t in hasilanalisis if t['sentimen']
                    == "Sentiment:: Positive :smiley:"]
    news_netral = [t for t in hasilanalisis if t['sentimen']
                   == "Sentiment:: Neutral 😐 "]
    news_negatif = [t for t in hasilanalisis if t['sentimen']
                    == "Sentiment:: Negative :angry:"]

    st.write('----------------------------------------------------------------')

    st.header("Hasil Persentase")
    try:
        st.write("positif : ", len(news_positif), "({} %)".format(
            100*len(news_positif)/len(hasilanalisis)))
        st.write("netral : ", len(news_netral), "({} %)".format(
            100*len(news_netral)/len(hasilanalisis)))
        st.write("negatif : ", len(news_negatif), "({} %)".format(
            100*len(news_negatif)/len(hasilanalisis)))
    except Exception as e:
        st.write("")

    # st.write('----------------------------------------------------------------')

    # st.write(hasilanalisis)
    # st.write(type(hasilanalisis))

    df_news = pd.DataFrame(hasilanalisis)
    # df_news
    # st.write(type(df_news))

    df_news_filter = df_news.dropna()

    df_filter1 = df_news_filter.loc[:, ['tanggal', 'sentimen', 'param']]
    # df_filter1
    # st.write(type(df_filter1))

    # st.write('----------------------------------------------------------------')
    # st.write("Count of Each group:")
    grouped_df = df_filter1.groupby(['tanggal', 'sentimen', 'param']
                                    ).size().reset_index(name="count_sentimen")

    grouped_df['nilaisentimen'] = grouped_df['param'] * \
        grouped_df['count_sentimen']

    # grouped_df
    # st.write(type(grouped_df))

    df_filter2 = grouped_df.loc[:, ['tanggal', 'nilaisentimen']]
    grouped_df2 = df_filter2.groupby(['tanggal']).sum()
    df_filter2
    grouped_df2
    df_filter2.to_csv('file_sentimen.csv', index=False)

    st.write('----------------------------------------------------------------')
    st.header("Chart Sentimen")
    st.line_chart(grouped_df2)

    # st.header("Sentimen Analisis")
    # fig = px.line(df_filter2[df_filter2['nilai'] == nilai],
    #               x="Tanggal", y="nilai", title=search)
    # st.plotly_chart(fig)

    # https://ksnugroho.medium.com/dasar-text-preprocessing-dengan-python-a4fa52608ffe

if selected == "Market Indonesia":
    ticker_symbol = st.sidebar.text_input('Stock Symbol :', '^JKSE')
    # st.sidebar.write(type(ticker_symbol))
    data_period = st.sidebar.text_input('Period :', '40d')
    # st.sidebar.write(type(data_period))
    data_interval = st.sidebar.radio(
        'Interval', ['1d', '5d', '15m', '30m', '1h'])
    # st.sidebar.write(type(data_interval))

    # st.header(ticker_symbol)
    if ticker_symbol == '^JKSE' or ticker_symbol == '':
        ticker_symbol2 = '^JKSE'
    else:
        ticker_symbol != '^JKSE'
        ticker_symbol2 = ticker_symbol+'.JK'

    ticker_data = util.get_ticker_data(
        ticker_symbol2, data_period, data_interval)
    # ticker_data
    # st.write(type(ticker_data))
    util.plot_candle_chart(ticker_data)


if selected == "Chart":
    with st.container():

        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Chart 1")
            df_sentimen = pd.read_csv("file_sentimen.csv")
            # df_sentimen
            # st.write(type(df_sentimen))

            fig = px.line(df_sentimen,
                          x="tanggal", y="nilaisentimen", title="Pencarian terakhir - Sentimen Analisis")
            st.plotly_chart(fig)

        with right_column:
            st.header("Chart 2")
            df_sentimen = pd.read_csv("file_sentimen.csv")
            # df_sentimen
            # st.write(type(df_sentimen))

            fig = px.line(df_sentimen,
                          x="tanggal", y="nilaisentimen", title="Pencarian terakhir - Sentimen Analisis")
            st.plotly_chart(fig)
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Chart 3")
            df_sentimen = pd.read_csv("file_sentimen.csv")
            # df_sentimen
            # st.write(type(df_sentimen))

            fig = px.line(df_sentimen,
                          x="tanggal", y="nilaisentimen", title="Pencarian terakhir - Sentimen Analisis")
            st.plotly_chart(fig)

        with right_column:
            st.header("Chart 4")
            df_sentimen = pd.read_csv("file_sentimen.csv")
            # df_sentimen
            # st.write(type(df_sentimen))

            fig = px.line(df_sentimen,
                          x="tanggal", y="nilaisentimen", title="Pencarian terakhir - Sentimen Analisis")
            st.plotly_chart(fig)
