import streamlit as st

######## for 1 asset ###########################
def calculate_asset_delta(df, asset_name):
  #new_name = str(asset_name)+'_delta'
  #### calculate chaange of asset value as a percentage of total value
  #df[new_name] = df[asset_name].diff()/df[asset_name]*100 
  df[asset_name] = df[asset_name].pct_change()*100 
  return df

######## for multiple assets ###################
def calculate_delta(df, asset_list):
  #st.write(df)
  #st.write(asset_list)
  df_delta = df
  for i in asset_list:
    asset_name = i
    df_delta = calculate_asset_delta(df_delta, asset_name)
  return df_delta

