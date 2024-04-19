import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from io import StringIO

# App title and data info
st.set_page_config(layout="wide")
st.title("Time Series Data App")


# Function to save uploaded file to session state
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Saving the bytes data in the session state
        st.session_state['uploaded_file'] =bytes_data
        return True
    return False

# File uploader widget
uploaded_file = st.file_uploader("Choose a file")
skiplines = st.number_input('Insert rows to skip',value=0)

# Check if we already have an uploaded file in the session state
if 'uploaded_file' not in st.session_state:
    if save_uploaded_file(uploaded_file):
        saved_file = st.session_state['uploaded_file']
        if uploaded_file.name.endswith('.txt'):
          data = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
          time_column = st.selectbox('select time column (x-axis)',data.columns)
          selected_col = st.selectbox("Select Column to Plot ((y-axis))", data.columns)
          data['Date']=data[time_column]
          
      # data = pd.read_csv(r'C:\Users\shiwa\Downloads\timeTEMP.txt', skiprows=1, delimiter='\t')
        elif uploaded_file.name.endswith('.csv'):
          data = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
          time_column = st.selectbox('select time column (x-axis)',data.columns)
          selected_col = st.selectbox("Select Column to Plot (y-axis)", data.columns)
          # data.columns = ["Date", f"{uploaded_file.name.split('.')[0]}"].append(data.columns[2:])
          data['Date']=data[time_column]
          
        if selected_col is not None and time_column is not None:

          data["Date"] = pd.to_datetime(data['Date'])
          st.write(data)  # Display the first few rows

          # Time series plot with plotly
            # Exclude 'Temperature'

          # Time range slider
          min_date = data['Date'].min().timestamp()
          max_date = data['Date'].max().timestamp()
          min_date_selected, max_date_selected = st.slider("Select Time Range",
                                                          min_value=datetime.datetime.fromtimestamp(min_date),
                                                          max_value=datetime.datetime.fromtimestamp(max_date),
                                                          value=(datetime.datetime.fromtimestamp(min_date), datetime.datetime.fromtimestamp(max_date)))

          # Filter data based on slider selection
          filtered_data = data.loc[(data['Date'] >= min_date_selected) & (data['Date'] <= max_date_selected)]

          # Create plotly figure
          fig = px.line(filtered_data, x='Date', y=selected_col,height=500,markers=False,color_discrete_sequence=['blue'],template='seaborn',title='Time Series Plotting')
          st.plotly_chart(fig,theme=None,use_container_width=True)

else:
  if uploaded_file:
    saved_file = st.session_state['uploaded_file']
    if uploaded_file.name.endswith('.txt'):
          data = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
          time_column = st.selectbox('select time column',data.columns)
          selected_col = st.selectbox("Select Column to Plot", data.columns)
          data['Date']=data[time_column]
          
      # data = pd.read_csv(r'C:\Users\shiwa\Downloads\timeTEMP.txt', skiprows=1, delimiter='\t')
    elif uploaded_file.name.endswith('.csv'):
          data = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
          time_column = st.selectbox('select time column',data.columns)
          selected_col = st.selectbox("Select Column to Plot", data.columns)
          # data.columns = ["Date", f"{uploaded_file.name.split('.')[0]}"].append(data.columns[2:])
          data['Date']=data[time_column]
    
    if selected_col is not None and time_column is not None:

      data["Date"] = pd.to_datetime(data['Date'])
      st.write(data)  # Display the first few rows

      # Time series plot with plotly
      # selected_col = st.selectbox("Select Column to Plot", data.columns[1:])  # Exclude 'Temperature'

      # Time range slider
      min_date = data['Date'].min().timestamp()
      max_date = data['Date'].max().timestamp()
      min_date_selected, max_date_selected = st.slider("Select Time Range",
                                                      min_value=datetime.datetime.fromtimestamp(min_date),
                                                      max_value=datetime.datetime.fromtimestamp(max_date),
                                                      value=(datetime.datetime.fromtimestamp(min_date), datetime.datetime.fromtimestamp(max_date)))

      # Filter data based on slider selection
      filtered_data = data.loc[(data['Date'] >= min_date_selected) & (data['Date'] <= max_date_selected)]

      # Create plotly figure
      fig = px.line(filtered_data, x='Date', y=selected_col,height=500,markers=False,color_discrete_sequence=['blue'],template='seaborn',title='Time Series Plotting')
      st.plotly_chart(fig,theme=None,use_container_width=True)
