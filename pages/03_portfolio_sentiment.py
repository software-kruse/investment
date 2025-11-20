import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as py
import numpy as np
import seaborn as sns

import function.get_price_data as price_data
import function.merge_price_data as merge_data

st.write(""" ## Portfolio sentiment  """)

st.write("""
plan for this page:
load dat for stocks, bonds and gold.
calculate an master-portfilio (e.g. 50/25/25).
calculate the rsi for each data point.
caluclate the average rsi for each category.
calcuate the delta between mean rsi and current rsi.
suggest a weighted portfolio, which has the master as a basis.
high rsi -> over balance
low rsi -> under balance
track performance if weigthed portfolio.
print portfolios against each other
analyse the portfolio based on metrics (sharpe, sortina, ...)
""")
