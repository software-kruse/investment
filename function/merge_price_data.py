import pandas as pd

#Funktion zum Kombinieren zweier Dataframes
def merge_data(data1, data2):
    data = pd.merge(data1, data2, on="Date", how="inner")    
    return data

def merge_data_outer(data1, data2):
    data = pd.merge(data1, data2, on="Date", how="outer")    
    return data
