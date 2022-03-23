# https://github.com/johnbumgarner/newspaper3_usage_overview
# https://pypi.org/project/gnews/
from pandas import period_range
import streamlit as st
from gnews import GNews
import json
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup
from textblob import TextBlob
from textblob import Word
import re
import pandas as pd
from datetime import datetime

google_news = GNews(language='id', country='ID', period='1', max_results=100,
                    exclude_websites=None)
indonesia_news = google_news.get_news("minyak goreng")
# print(indonesia_news[0])

# for news in indonesia_news:
# print(news['title'])
# st.write(f"Judul :{news['title']} \n link:{news['url']}\n\n")

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'

config = Config()
config.browser_user_agent = USER_AGENT
config.request_timeout = 10

st.dataframe(indonesia_news)


# for i in range(7):

#     hasilanalisis = []
#     today = DT.date.today()
#     dayH = today - DT.timedelta(days=i)
#     dayMinuteOne = dayH - DT.timedelta(days=1)
#     st.write(str(dayH))
hasilanalisis = []

try:
    for news in indonesia_news:
        # st.write(news['title'])
        # st.write(news['description'])
        base_url = news['url']
        article = Article(base_url, config=config)

        article.download()
        article.parse()

        publish_date = article.publish_date

        st.write(publish_date)
        st.write(article.title)
        article_meta_data = article.meta_data
        # st.write(article.meta_data)
        article_summary = {value for (
            key, value) in article_meta_data.items() if key == 'description'}
        st.write(article_summary)
        # st.write(base_url)
        news_properties = {}
        news_properties["title"] = article.title
        news_properties["tanggal"] = publish_date.strftime('%Y-%m-%d')
        news_properties["isi_news"] = article_summary
        news_nilai = ' '.join(re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(article_summary)).split())
        st.write(base_url)
        analysis = TextBlob(news_nilai)
        # st.write(analysis)
        analysis = analysis.translate(to="en")
        # st.write(analysis)

        st.write(analysis.sentiment.polarity)

        if analysis.sentiment.polarity > 0.0:
            news_properties['sentimen'] = "Sentiment:: Positive :smiley:"
        elif analysis.sentiment.polarity == 0.0:
            news_properties['sentimen'] = "Sentiment:: Neutral 😐 "
        else:
            news_properties['sentimen'] = "Sentiment:: Negative :angry:"

        st.write(news_properties['sentimen'])
        # st.write(news_properties)

        hasilanalisis.append(news_properties)

    # print(type(news_properties))
    # print(news_properties)

    # df_news = pd.DataFrame(news_properties)
    # print(df_news)


except Exception as e:
    print("something error")

news_positif = [t for t in hasilanalisis if t['sentimen']
                == "Sentiment:: Positive :smiley:"]
news_netral = [t for t in hasilanalisis if t['sentimen']
               == "Sentiment:: Neutral 😐 "]
news_negatif = [t for t in hasilanalisis if t['sentimen']
                == "Sentiment:: Negative :angry:"]

st.write("hasil sentimen")
st.write("positif : ", len(news_positif))
st.write("netral : ", len(news_netral))
st.write("negatif : ", len(news_negatif))

# print(type(hasilanalisis))
# print(hasilanalisis)

# df_news = pd.DataFrame(hasilanalisis, columns=[
#                        'title', 'tanggal', 'isi_news', 'sentimen'], dtype=float)
# st.dataframe(df_news)

df_news = pd.DataFrame(hasilanalisis, columns=[
    'tanggal',  'sentimen'])
# st.dataframe(df_news)

# st.dataframe(df_news.value_counts())

dfgroup_news = pd.DataFrame(df_news.value_counts())

st.dataframe(dfgroup_news)

# grouped_df = df_news.groupby(["tanggal", "sentimen"])

# for key, item in grouped_df:
#     a_group = grouped_df.get_group(key)
#     st.write(a_group, "\n")

# group tanggal, sentiment , count(*)


# df_news = pd.dataframe(hasilanalisis)
# st.dataframe(df_news)
