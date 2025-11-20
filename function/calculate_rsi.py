def calculate_rsi(df, timeframe=100, asset_name='Close', column_name='RSI'):
  #rsi calculation 
  timeframe_rsi = timeframe
  delta = df[asset_name].diff()
  up = delta.clip(lower=0)
  down = -1*delta.clip(upper=0)
  ema_up = up.ewm(com=timeframe_rsi, adjust=False).mean()
  ema_down = down.ewm(com=timeframe_rsi, adjust=False).mean()
  rs = ema_up/ema_down
  df = df[timeframe_rsi:]
  df[column_name] = 100 - (100/(1 + rs))
  return df
