import yfinance as yf


def get_ticker_data(ticker_symbol, data_period, data_interval):
    ticker_data = yf.download(ticker_symbol, data_period, data_interval)

    if len(ticker_data) == 0:
        st.write("ticker kosong")
