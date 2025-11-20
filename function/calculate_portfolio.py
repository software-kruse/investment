import streamlit as st
import pandas as pd
import numpy as np

import function.calculate_rsi as rsi

# helpful page: https://www.askpython.com/python-modules/pandas/update-the-value-of-a-row-dataframe

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################

### Calculate portfolio return - time based rebalancing
def calculate_return(df, df_weight, asset_list,rebalancing_period):
  # copy original df
  df_return = df.copy()
  # set the start amount
  start_amount = 1000
  #easy iteration
  for i in range(len(df_return)):
    # get the index from df_return - these are the dates
    index_list = df_return.index.values.tolist()
    # set initial weights
    if i == 0:
      # create list to store initial amounts
      inital_amount = [None]*len(asset_list)
      for j in range(len(asset_list)):
        # get percentage of weight from df_weight
        temp_percentage = df_weight.iloc[j]['weight']
        # calculate inital amount as a total value
        inital_amount[j] = start_amount*temp_percentage/100
        # assign amount to first row of df_return
        df_return.loc[index_list[0],asset_list[j]] = inital_amount[j]    
    # calculate change of value
    elif i % rebalancing_period == 0 and i != 0:
      # create list to store new amounts
      new_amount = [None]*len(asset_list)
      # new variable to store the total portfolio value for this week
      total_return_temp = 0
      for j in range(len(asset_list)):
        temp_multiplier = (df_return.iloc[i][asset_list[j]] / 100 ) + 1.0
        previous_value = df_return.iloc[i-1][asset_list[j]] 
        # calcualte the new week value, but don't assign to df
        new_value_temp = temp_multiplier * previous_value
        # store value to temp variable instead
        total_return_temp = total_return_temp + new_value_temp
      for j in range(len(asset_list)):
        # get percentage of weight from df_weight
        temp_percentage = df_weight.iloc[j]['weight']
        # calculate new amount as a total value from temp variable
        new_amount[j] = total_return_temp*temp_percentage/100
        # assign amount to this row of df_return
        df_return.loc[index_list[i],asset_list[j]] = new_amount[j]      
    else:
      # i iterating the df_return lenght
      for j in range(len(asset_list)):
        # get change of value as percentage
        temp_multiplier = (df_return.iloc[i][asset_list[j]] / 100 ) + 1.0
        # get previous amount from week before
        previous_value = df_return.iloc[i-1][asset_list[j]] 
        # calculate amount for this week and assign to df
        df_return.loc[index_list[i],asset_list[j]] = temp_multiplier * previous_value
  return df_return


###########################################################################################################################
###########################################################################################################################
###########################################################################################################################

################# NOT FINISHED YET!!! ################################################
### Calculate portfolio return - rsi based rebalancing
def calculate_return_rsi(df, df_weight, asset_list, rsi_high=70, rsi_low=30):
  # copy original df
  df_return = df.copy()
  # set the start amount
  start_amount = 1000
  
  ### step 1 - create df with return values
  for i in range(len(df_return)):
    # get the index from df_return - these are the dates
    index_list = df_return.index.values.tolist()
    # set initial weights
    if i == 0:
      # create list to store initial amounts 
      inital_amount = [None]*len(asset_list)
      for j in range(len(asset_list)):
        # get percentage of weight from df_weight
        temp_percentage = df_weight.iloc[j]['weight']
        # calculate inital amount as a total value
        inital_amount[j] = start_amount*temp_percentage/100
        # assign amount to first row of df_return
        df_return.loc[index_list[0],asset_list[j]] = inital_amount[j]    
    # calculate following values       
    else:
      # i iterating the df_return lenght
      for j in range(len(asset_list)):
        # get change of value as percentage
        temp_multiplier = (df_return.iloc[i][asset_list[j]] / 100 ) + 1.0
        # get previous amount from week before
        previous_value = df_return.iloc[i-1][asset_list[j]] 
        # calculate amount for this week and assign to df
        df_return.loc[index_list[i],asset_list[j]] = temp_multiplier * previous_value
        
  ### step 2 - calculate rsi values for each column
  for j in range(len(asset_list)):
    asset = str(j)
    df_return = calculate_rsi.calculate_rsi(df_return, 100, asset_name=asset, column_name='RSI-'+asset)
    
  ### step 3 - rebalance, if rsi to high/low
  iteration_counter = len(df_return)
  if i < iteration_counter:
    if i > 100 and (df_return.iloc[i]['RSI'] > upper_limit or df_return.iloc[i]['RSI'] < lower_limit):
      # create list to store new amounts
      new_amount = [None]*len(asset_list)
      # new variable to store the total portfolio value for this week
      total_return_temp = 0
      for j in range(len(asset_list)):
        temp_multiplier = (df_return.iloc[i][asset_list[j]] / 100 ) + 1.0
        previous_value = df_return.iloc[i-1][asset_list[j]] 
        # calcualte the new week value, but don't assign to df
        new_value_temp = temp_multiplier * previous_value
        # store value to temp variable instead
        total_return_temp = total_return_temp + new_value_temp
      for j in range(len(asset_list)):
        # get percentage of weight from df_weight
        temp_percentage = df_weight.iloc[j]['weight']
        # calculate new amount as a total value from temp variable
        new_amount[j] = total_return_temp*temp_percentage/100
        # assign amount to this row of df_return
        df_return.loc[index_list[i],asset_list[j]] = new_amount[j]
      i=i+1
    if i == (iteration_counter-1):
      i = i
      #check if rsi ok, otherwise reset the loop
  ################# NOT FINISHED YET!!! ################################################     
  return df_return

