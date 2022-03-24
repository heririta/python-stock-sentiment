import pandas as pd  # pip install pandas openpyxl
from pathlib import Path  # Python Standard Library
import requests
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from urllib.request import Request, urlopen
import lxml

req = Request('https://www.cnbcindonesia.com',
              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'})
webpage = urlopen(req)

data = pd.read_html(webpage)

# st.markdown('Header in Website BI 7-day (Reverse) Repo Rate ')

# df = data[0]
# df
# df_header = df.columns
# st.dataframe(df_header)
# st.write(f"count header web : {len(df_header)}")
