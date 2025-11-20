import numpy as np

# https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python
# return_series = df
# N = number of intervals in 1 year, if weekly data = 52
# rf = risk free rate, e.g. 0.01

# calculates the mean return for the complete data
def mean_return(return_series, N):
  mean = return_series.mean() * N
  return mean

# calculates the mean return only for a certain time frame
def return_rolling(df, timeframe):
  df_ret = df.copy()
  for column in df_ret:
      df_ret[column] = df_ret[column].rolling(timeframe).apply(lambda x: (x.mean()*timeframe), raw = True)
      df_ret.fillna(0, inplace = True)
  df_ret = df_ret[timeframe:]
  return df_ret

# calculates the sharpe ratio for the complete data
def sharpe_ratio(return_series, N, rf):
  mean = return_series.mean() * N -rf
  sigma = return_series.std() * np.sqrt(N)
  return mean / sigma

# calculates the sharpe ratio only for a certain time frame
def sharpe_rolling(df, N, rf, timeframe):
  df_sr = df.copy()
  for column in df_sr:
      df_sr[column] = df_sr[column].rolling(timeframe).apply(lambda x: (x.mean()*N-rf)/(x.std()*np.sqrt(N)), raw = True)
      df_sr.fillna(0, inplace = True)
  df_sr = df_sr[timeframe:]
  return df_sr

def sortino_ratio(series, N,rf):
  mean = series.mean() * N -rf
  std_neg = series[series<0].std()*np.sqrt(N)
  return mean/std_neg

def max_drawdown(return_series):
  comp_ret = (return_series+1).cumprod()
  peak = comp_ret.expanding(min_periods=1).max()
  dd = (comp_ret/peak)-1
  return dd.min()

def calmars(return_series, N, max_drawdowns):
  calmars = return_series.mean()*N/abs(max_drawdowns)
  return calmars
