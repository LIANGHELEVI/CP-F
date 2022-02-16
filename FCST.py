import streamlit as st
import datetime
import pandas as pd
import time

import numpy as np
import matplotlib.pyplot as plt
import plotly
import altair as alt

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, make_scorer
#mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import cross_val_score

import scipy
import yfinance as yf

st.title("Cotton Price Trend Preciation")
st.header("A Basic Data Science Web Application")
st.sidebar.header("ML Bootcamp \n Graduates Production")


# Update Yesterday Date
Yesterday=datetime.datetime.now()-datetime.timedelta(days=1)

#Download from Yahoo finance (Cotton Price)
ticker="CT=F"
period1=int(time.mktime(datetime.datetime(2000,3,1,23,59).timetuple()))
period2=int(time.mktime(Yesterday.timetuple())) # To update with latest date
interval='1d' #1wk,1m

query_string=f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
# pd.options.display.float_format = '${:,.2f}'.format
dfy=pd.read_csv(query_string,parse_dates=['Date'],index_col="Date")
dfy=dfy.dropna()
dfy=dfy.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
dfy.index = dfy.index.strftime('%Y-%m-%d')
# dfy['Adj Close']=dfy['Adj Close'].map('${:,.2f}'.format)

#Download from Yahoo finance (Crude Oil Price)
ticker_o="CL=F"

query_string_o=f'https://query1.finance.yahoo.com/v7/finance/download/{ticker_o}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'

dfy_o=pd.read_csv(query_string_o,parse_dates=['Date'],index_col="Date")
dfy_o=dfy_o.dropna()
dfy_o=dfy_o.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
dfy_o.index = dfy_o.index.strftime('%Y-%m-%d')
# dfy_o['Adj Close']=dfy_o['Adj Close'].map('${:,.2f}'.format)

chart_data_table=pd.merge(dfy['Adj Close'].map('{:,.2f}'.format),dfy_o['Adj Close'].map('{:,.2f}'.format), left_index=True, right_index=True, suffixes=("_Cotton", "_Crude Oil"),).apply(pd.to_numeric)


st.subheader('Cotton & Crude Oil Price')
st.table(chart_data_table.tail(7))
print(chart_data_table.info())


# 2021 onwards
st.subheader('Price Evolution 2021 Onwards')
st.line_chart(chart_data_table)

