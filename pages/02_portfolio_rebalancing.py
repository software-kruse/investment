import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

import function.get_price_data as price_data
import function.merge_price_data as merge_data
import function.visualize_price_data as vpd
import function.get_price_delta as price_delta
import function.calculate_rsi as rsi
import function.calculate_portfolio as portfolio
import function.calculate_ratio as ratio

st.write(' ## Rebalancing Effect Information')
exp_info = st.expander("Show general information about rebalancing effect", expanded=True)
exp_info.write('Easy visualisation https://www.farmersfable.org/')
exp_info.write('Preconditions for the shown example:')
exp_info.write('1.) similar/equal return')
exp_info.write('2.) no correlation')

############################################################################################
st.write(' ## Portfolio Rebalancing Simulation')

### load available options
df = pd.read_excel("data/ticker.xlsx")
exp_01 = st.expander("Show complete reference data", expanded=False)
exp_01.write(df)

### select the options you want to have
name_arr = df['name'].to_numpy()
selected_names = st.multiselect('What do you want to include?',name_arr)
st.write('You selected:', selected_names)

############################################################################################
### set the weights you want to have
### Mit df lösen, 2. Spalte für Gewichtungen
def set_weights(selected_names,exp_weights):
  #Neuen DF anlegen für die Schleife
  df_weight = pd.DataFrame(columns=["asset","weight"])
  #Aufbau der Auswahlmenüs
  for i in range(len(selected_names)):
    a = exp_weights.number_input('Choose the weight of '+str(selected_names[i]), value=0)
    new_row = {"asset":str(selected_names[i]), "weight":a}
    df_weight.loc[i] = new_row
  return df_weight

############################################################################################
### get all data from yfinance
def get_calculation_data(df,selected_names):
  ### Analyse choosen options and get data
  temp_int = 0
  for i in selected_names:
    temp_name = i
    temp_list = df.index[df['name'] == i].tolist()
    temp_index = temp_list[0]
    temp_ticker = df.iloc[temp_index]['ticker']
    if temp_int == 0:
      data = price_data.get_ydata(temp_ticker,temp_name)
      data['Date'] = pd.to_datetime(data['Date'])
      data['Date'] = data['Date'].dt.strftime('%Y%m%d')
      data = data.set_index("Date")
    else:
      temp_data = price_data.get_ydata(temp_ticker,temp_name)
      temp_data['Date'] = pd.to_datetime(temp_data['Date'])
      temp_data['Date'] = temp_data['Date'].dt.strftime('%Y%m%d')
      temp_data = temp_data.set_index("Date")
      data = merge_data.merge_data(data, temp_data)
      #data.join(temp_data, how='outer')
    temp_int = temp_int + 1
  return data

############################################################################################
### Button to choose weights
check_box_1 = st.checkbox('1 - Have you choosen all assets?')
if check_box_1:
  exp_weights = st.expander("Enter the weights you want to have", expanded=False)
  # create menu for choosing weights
  df_weight = set_weights(selected_names, exp_weights)
  # show the percentages
  df_weight.set_index('asset', inplace = True)
  #st.write(df_weight)
  # calculate sthe sum of all values
  exp_weights.write(df_weight.sum())

############################################################################################    
### Button to start the simulation 
check_box_2 = st.checkbox('2 - Do you want get the data for these weights?')
if check_box_2:
#if st.button('get price data'):
  data = get_calculation_data(df,selected_names)
  df_delta = price_delta.calculate_delta(data,selected_names)
  # visualize the data
  exp_delta_price = st.expander("Show visualized price movement data", expanded=False)
  exp_delta_price.line_chart(df_delta)
  #exp_delta_price.vpd.visualize_data(df_delta, style='lin', normalize='no')
  exp_delta_price.write(df_delta)
    
############################################################################################    
### Button calculate returns
check_box_3 = st.checkbox('3 - Do you want to calculate the returns?')
if check_box_3:
  # rebalancing period in weeks
  df_1_weeks = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 1)
  df_4_weeks = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 4)
  df_12_weeks = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 12)
  df_26_weeks = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 26)
  df_52_weeks = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 52)
  df_no_rebalancing = portfolio.calculate_return(df_delta, df_weight, selected_names, rebalancing_period = 100000)
  #df_rsi_rebalancing = portfolio.calculate_return_rsi(df_delta, df_weight, selected_names, rsi_high=70, rsi_low=30)
  # sum up all rows into new total column
  df_1_weeks['1_week'] = df_1_weeks.sum(axis=1)
  df_4_weeks['1_month'] = df_4_weeks.sum(axis='columns')
  df_12_weeks['3_month'] = df_12_weeks.sum(axis=1)
  df_26_weeks['6_month'] = df_26_weeks.sum(axis=1)
  df_52_weeks['1_year'] = df_52_weeks.sum(axis=1)
  df_no_rebalancing['no_rebalancing'] = df_no_rebalancing.sum(axis=1)
  #df_rsi_rebalancing['rsi_rebalancing'] = df_rsi_rebalancing.sum(axis=1)
  # delete asset columns 
  df_1_weeks_sum = df_1_weeks[['1_week']]
  df_4_weeks_sum = df_4_weeks[['1_month']]
  df_12_weeks_sum = df_12_weeks[['3_month']]
  df_26_weeks_sum = df_26_weeks[['6_month']]
  df_52_weeks_sum = df_52_weeks[['1_year']]
  df_no_rebalancing_sum = df_no_rebalancing['no_rebalancing']
  #df_rsi_rebalancing_sum = df_rsi_rebalancing['rsi_rebalancing']
  # merge df
  df_return = pd.concat([df_1_weeks_sum, df_4_weeks_sum], axis=1, join="inner")
  df_return = pd.concat([df_return, df_12_weeks_sum], axis=1, join="inner")
  df_return = pd.concat([df_return, df_26_weeks_sum], axis=1, join="inner")
  df_return = pd.concat([df_return, df_52_weeks_sum], axis=1, join="inner")
  df_return = pd.concat([df_return, df_no_rebalancing_sum], axis=1, join="inner")
  #df_return = pd.concat([df_return, df_rsi_rebalancing_sum], axis=1, join="inner")
  # add expander for visualization
  exp_return = st.expander("Show visualized portfolio data", expanded=False)
  # choose benchmark asset
  benchmark_name = exp_return.selectbox('Do you want to add a benchmark?',name_arr)
  benchmark_list = df.index[df['name'] == benchmark_name].tolist()
  benchmark_index = benchmark_list[0]
  benchmark_ticker = df.iloc[benchmark_index]['ticker']
  # button to update benchmark data
  if exp_return.button('update benchmark data'):
    # get and prepare data
    benchmark_data = price_data.get_ydata(benchmark_ticker,benchmark_name)
    benchmark_data['Date'] = pd.to_datetime(benchmark_data['Date'])
    benchmark_data['Date'] = benchmark_data['Date'].dt.strftime('%Y%m%d')
    benchmark_data = benchmark_data.set_index("Date")
    # merge data
    df_return = merge_data.merge_data(df_return, benchmark_data)
    df_return = (df_return/df_return.iloc[0])*1000
  # visualize the results  
  exp_return.line_chart(df_return)
  exp_return.write(df_return)
  # visualize additional information
  exp_return_info = st.expander("Show additional price information", expanded=False)
  exp_return_info.write('### 1 week')
  exp_return_info.write(df_1_weeks)
  exp_return_info.write('### 1 month')
  exp_return_info.write(df_4_weeks)
  exp_return_info.write('### 3 month')
  exp_return_info.write(df_12_weeks)
  exp_return_info.write('### 6 month')
  exp_return_info.write(df_26_weeks)
  exp_return_info.write('### 1 year')
  exp_return_info.write(df_52_weeks)
  exp_return_info.write('### no rebalancing')
  exp_return_info.write(df_no_rebalancing)
  #exp_return_info.write('### rsi rebalancing')
  #exp_return_info.write(df_rsi_rebalancing)

############################################################################################    
### Button calculate ratios for all portfolios
check_box_4 = st.checkbox('4 - Do you want to calculate some ratios?')
if check_box_4:
  # create a df to calculate ratios
  df_ratio = df_return.copy()
  df_ratio = df_ratio.pct_change()
  # enter input values for your settings
  N = 52
  rf = 0.00
  # calculate mean return
  #mean_return = df_ratio.apply(ratio.mean_return, args=(N),axis=0)
  mean_return = df_ratio.apply(ratio.mean_return, args=(N,) ,axis=0)
  # calculate the ratios
  sharpes = df_ratio.apply(ratio.sharpe_ratio, args=(N,rf,),axis=0)
  #st.write(sharpes)
  sortinos = df_ratio.apply(ratio.sortino_ratio, args=(N,rf,), axis=0)
  #st.write(sortinos)
  max_drawdowns = df_ratio.apply(ratio.max_drawdown,axis=0)
  #st.write(max_drawdowns)
  #calmars = df_return.apply(ratio.calmars, args=(N,max_drawdowns,), axis=0)
  calmars = df_ratio.mean()*N/abs(max_drawdowns)
  #st.write(calmars)
  # combine ratios to a df
  portfolio_ratios = pd.DataFrame()
  portfolio_ratios['mean_return'] = mean_return
  portfolio_ratios['sharpe'] = sharpes
  portfolio_ratios['sortino'] = sortinos  
  portfolio_ratios['max_drawdown'] = max_drawdowns
  portfolio_ratios['calmar'] = calmars
  # visualize everything
  exp_ratio = st.expander("Show ratio information", expanded=False)
  exp_ratio.bar_chart(portfolio_ratios)
  portfolio_ratios = portfolio_ratios.T
  exp_ratio.line_chart(portfolio_ratios) 
  exp_ratio.write(portfolio_ratios)

############################################################################################    
### Button calculate rolling metrics
check_box_5 = st.checkbox('5 - Do you want more information?')
if check_box_5:
  # enter input values for your settings
  N = 52
  rf = 0.00
  timeframe = 200
  # create a df to calculate rolling  ratios
  df_rolling = df_return.copy()
  df_rolling = df_rolling.pct_change()
  # visualize everything
  exp_add_info = st.expander("Show additional information", expanded=False)
  
  # apply rolling sharpe ratio to df
  df_sr =  ratio.sharpe_rolling(df_rolling, N, rf, timeframe)
  exp_add_info.write('### '+str(timeframe)+' week rolling sharpe ratio') 
  exp_add_info.line_chart(df_sr) 
  exp_add_info.write(df_sr)
  # get mean values
  exp_add_info.write('### Average of '+str(timeframe)+' week rolling sharpe ratio') 
  exp_add_info.bar_chart(df_sr.mean())
  #exp_add_info.write(df_sr.mean())
  
  # apply rolling return to df
  df_ret =  ratio.return_rolling(df_rolling, timeframe)
  exp_add_info.write('### '+str(timeframe)+' week mean return') 
  exp_add_info.line_chart(df_ret) 
  # get mean values
  exp_add_info.write('### Average of '+str(timeframe)+' week mean return') 
  exp_add_info.bar_chart(df_ret.mean())
