import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as py
import numpy as np
import seaborn as sns

import function.get_price_data as price_data
import function.merge_price_data as merge_data

st.write(""" ## Sharpe ratio  """)

### load available options
df = pd.read_excel("data/ticker.xlsx")
exp_01 = st.expander("Show complete reference data", expanded=False)
exp_01.write(df)

### create list from data
name_arr = df['name'].to_numpy()

### select the options you want to have
selected_names = st.multiselect('What do you want to include?',name_arr)
st.write('You selected:', selected_names)

### select number of iterations
iteration_number = st.slider('How many iterrations should be calculated?', 0, 100000, 30000)
### select risk free rate
risk_free_rate = st.slider('What can be considered as the risk free rate? [%]', 0.0, 1.0, 4.0) / 100


### get all data
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
  ### show data    
  try:
    st.write(data)   
  except:
    st.write('Choose assets ...')
  return data

### visualization of price data
def visualize_data(data):
  try:
    #st.write(data.iloc[0])
    data = data/data.iloc[0]
    fig1, (ax1) = plt.subplots(1,1)
    for col in data.columns:
        column_name = (col)
        ax1.semilogy(data[column_name], zorder = 2, linewidth=1, label=column_name)
    #ax1.grid()  
    ax1.legend(loc="upper left")
    #fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
    exp_02 = st.expander("Show visualized price data", expanded=False)
    exp_02.write('### logarithmic scale')
    exp_02.pyplot(fig1)
    exp_02.write('### linear scale')
    exp_02.line_chart(data)
  except:
    st.write('No visualization possible...')
    
    
### calculation of sharpe ratios    
def calculate_sharpe_ratios(data):  
  
  ### calculate return
  data_ret = data.pct_change()
  exp_ret = st.expander("Show returns", expanded=False)
  exp_ret.write(data_ret)  
  
  ### calculate mean returns
  st.write('### Mean return')
  data_mean_ret = data_ret.mean()*52 #52weeks
  st.write(data_mean_ret)
  
  ### create covariance matrix
  st.write('### covariance matrix')
  cov_matrix = data_ret.cov()
  st.write(cov_matrix)
  
  ### create correlation matrix
  st.write('### correlation matrix')
  cor_matrix = data_ret.corr()
  st.write(cor_matrix) 
  
  ### correlation heatmap
  cor_heatmap = plt.figure()
  sns.heatmap(cor_matrix,vmin=-1.0, vmax=1.0,cmap="coolwarm")
  st.pyplot(cor_heatmap)
  
  ### give names to calculation function
  stocks=selected_names  
  
  ### set iteration number
  simulation_result = np.zeros((3+len(stocks),iteration_number))
  
  ### iterate calculation
  for i in range(iteration_number):
    weights = np.array(np.random.random(len(stocks)))
    weights = weights/np.sum(weights)
    
    portfolio_return = np.sum(data_mean_ret * weights) 
    portfolio_std_dev = np.dot(weights.T,np.dot(cor_matrix,weights)) 
        
    simulation_result[0,i] = portfolio_return
    simulation_result[1,i] = portfolio_std_dev
    simulation_result[2,i] = (simulation_result[0,i] - risk_free_rate) / simulation_result[1,i]
    
    for j in range(len(weights)):
        simulation_result[j+3,i] = weights[j]
        
  ### store calculation in df
  column_list = ["avg-ret","std","sharpe"] + stocks
  df_plot = pd.DataFrame(simulation_result.T,columns=column_list)
  
  ### find best result
  search_column = df_plot["sharpe"]
  search_value = search_column.max()
  search_index = search_column.idxmax()
  df_optimum = df_plot.iloc[[search_index]]
  st.write(' ### optimized result')
  st.write(df_optimum)
  
  ### pie chart
  optimum_list = df_optimum.loc[search_index, :].values.flatten().tolist()
  del  optimum_list[0:3]  
  #st.write(optimum_list)
  #st.write(stocks)
  pie_fig, ax_pie = plt.subplots()
  ax_pie.pie(optimum_list, labels=stocks, autopct='%1.1f%%',shadow=False, startangle=90)
  ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  st.pyplot(pie_fig)
                                                
  ### plot graph
  fig = py.scatter(df_plot, x="std", y="avg-ret", color="sharpe", color_continuous_scale='Inferno', hover_data=stocks) 
  fig.update_xaxes(title_text="Volatility", title_font_size=10)
  fig.update_yaxes(title_text="Average Return in %", title_font_size=10)
  st.plotly_chart(fig)

if st.button('calculate optimal portfolio'):
  data = get_calculation_data(df,selected_names)
  visualize_data(data)  
  calculate_sharpe_ratios(data)

else:
   st.write('')
