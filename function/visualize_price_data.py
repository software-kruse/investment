import streamlit as st
import matplotlib.pyplot as plt

### visualization of price data ###

def visualize_data(data, style='log', normalize='no'):
  try:
    ### Start all lines at the same point? ###
    if normalize == 'yes':
      #st.write(data.iloc[0])
      data = data/data.iloc[0]
      
    ### Start figure creation ###
    fig1, (ax1) = plt.subplots(1,1)
    for col in data.columns:
        column_name = (col)
        ### Use a logarithmic scale? ###
        if style == 'log':
          ax1.semilogy(data[column_name], zorder = 2, linewidth=1, label=column_name)
        else:
          ax1.plot(data[column_name], zorder = 2, linewidth=1, label=column_name)
          
    ### Other options ###      
    #ax1.grid()  
    ax1.legend(loc="upper left")
    #fig1.update_layout(xaxis={'visible': False, 'showticklabels': False})
    
    ### Insert visualization into streamlit ###
    #expander_name = st.expander("Show visualized data", expanded=False)
    #expander_name.pyplot(fig1)
    with st.expander("Show visualized data"):
      st.pyplot(fig1)
    
  except:
    st.write('No visualization possible...')
