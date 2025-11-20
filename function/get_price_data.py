import yfinance as yf
import pandas as pd

#Funktion zum Laden von Daten von Yahoo Finance
def get_ydata(ticker, name='Close', interval='1wk'):
  try:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Adj Close"]] #1wk
    data = data.rename(columns={"Adj Close":name})
  except:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Close"]] #1wk
    data = data.rename(columns={"Close":name})
  return data

#Funktion zum Laden von Daten mit normalisierten Preisen
def get_normalized_ydata(ticker, name='Close', interval='1wk'):
  try:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Adj Close"]] #1wk
    data = data.rename(columns={"Adj Close":name})
  except:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Close"]] #1wk
    data = data.rename(columns={"Close":name})      
  data[name] = data[name]/data[name].iloc[0]
  return data  

#Funktion zum Laden von Daten mit normalisierten Datumsangaben
def get_ydata_test(ticker, name='Close', interval='1wk'):
  try:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Adj Close"]] #1wk
    data = data.rename(columns={"Adj Close":name})
  except:
    data = yf.Ticker(ticker).history(period="max", interval=interval).reset_index()[["Date","Close"]] #1wk
    data = data.rename(columns={"Close":name})      
  # Set universal data index  
  data['Date'] = pd.to_datetime(data['Date'])
  data['Date'] = data['Date'].dt.strftime('%Y%m%d')
  data = data.set_index("Date")
  data.index = pd.to_datetime(data.index)
  #data = data.set_index("Date")
  return data

     
