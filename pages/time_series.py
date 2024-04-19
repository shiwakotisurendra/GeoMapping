import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from io import StringIO

# App title and data info
st.set_page_config(layout="wide")
st.title("Data Analytics App")


# Function to save uploaded file to session state
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Saving the bytes data in the session state
        st.session_state[f'{uploaded_file.name}'] =bytes_data
    #     return True
    # return False

# File uploader widget
uploaded_file = st.file_uploader("Choose a file")
skiplines = st.number_input('Insert rows to skip',value=0)
plotting_options = st.selectbox('select type of the plot', ['time_series','line_plot','bar_plot', 'scatter_plot','box_plot','piechart_plot','hist_plot'],placeholder='select plot',index=None)

# Check if we already have an uploaded file in the session state

def plot_time_series():
  if uploaded_file.name not in st.session_state and plotting_options == 'time_series':
    save_uploaded_file(uploaded_file)
    saved_file = st.session_state[f'{uploaded_file.name}']
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
    if uploaded_file and plotting_options == 'time_series':
      saved_file = st.session_state[f'{uploaded_file.name}']
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
        
        
def line_plot_options():

  if uploaded_file.name not in st.session_state and plotting_options == 'line_plot':
    save_uploaded_file(uploaded_file)
    saved_file = st.session_state[f'{uploaded_file.name}']
    if uploaded_file.name.endswith('.txt'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
      st.write(df_line.head())
      x_column = st.selectbox('select time column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
    elif uploaded_file.name.endswith('.csv'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
      st.write(df_line.head())
      x_column = st.selectbox('select time column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
    
    if x_column is not None and y_column is not None:
      fig = px.line(df_line, x=x_column, y=y_column,height=500,markers=False,color_discrete_sequence=['blue'],template='seaborn',title='Time Series Plotting')
      st.plotly_chart(fig,theme=None,use_container_width=True)
  else:
    if uploaded_file and plotting_options == 'line_plot':
      saved_file = st.session_state[f'{uploaded_file.name}']
      if uploaded_file.name.endswith('.txt'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
        st.write(df_line.head())
        x_column = st.selectbox('select time column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        
      elif uploaded_file.name.endswith('.csv'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
        st.write(df_line.head())
        x_column = st.selectbox('select time column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        
      if x_column is not None and y_column is not None:
        fig = px.line(df_line, x=x_column, y=y_column,height=500,markers=True,color_discrete_sequence=['brown'],template='seaborn',title='Line Plotting')
        st.plotly_chart(fig,theme=None,use_container_width=True)
        
def bar_plot_options():
  if uploaded_file.name not in st.session_state and plotting_options == 'bar_plot':
    save_uploaded_file(uploaded_file)
    saved_file = st.session_state[f'{uploaded_file.name}']
    if uploaded_file.name.endswith('.txt'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
      st.write(df_line.head())
      x_column = st.selectbox('select time column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
      color_column = st.selectbox("Select color column", df_line.columns)
    elif uploaded_file.name.endswith('.csv'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
      st.write(df_line.head())
      x_column = st.selectbox('select X column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Y column (y-axis)", df_line.columns)
      color_column = st.selectbox("Select color column", df_line.columns)
    
    if x_column is not None and y_column is not None:
      fig = px.bar(df_line, x=x_column, y=y_column,height=500,color=color_column,color_discrete_sequence=['blue'],template='plotly_dark',title='Time Series Plotting')
      st.plotly_chart(fig,theme=None,use_container_width=True)
  else:
    if uploaded_file and plotting_options == 'bar_plot':
      saved_file = st.session_state[f'{uploaded_file.name}']
      if uploaded_file.name.endswith('.txt'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
        st.write(df_line.head())
        x_column = st.selectbox('select time column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        color_column = st.selectbox("Select color column", df_line.columns)
        
      elif uploaded_file.name.endswith('.csv'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
        st.write(df_line.head())
        x_column = st.selectbox('select time column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        color_column = st.selectbox("Select color column", df_line.columns)
        
      if x_column is not None and y_column is not None:
        fig = px.bar(df_line, x=x_column, y=y_column,color=color_column,height=500, template='plotly_dark',title='Bar Plotting')
        st.plotly_chart(fig,theme=None,use_container_width=True)
        
def scatter_plot_options():
  if uploaded_file.name not in st.session_state and plotting_options == 'scatter_plot':
    save_uploaded_file(uploaded_file)
    saved_file = st.session_state[f'{uploaded_file.name}']
    if uploaded_file.name.endswith('.txt'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
      st.write(df_line.head())
      x_column = st.selectbox('select X column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
      color_column = st.selectbox("Select color column", df_line.columns)
    elif uploaded_file.name.endswith('.csv'):
      df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
      st.write(df_line.head())
      x_column = st.selectbox('select X column (x-axis)',df_line.columns)
      y_column = st.selectbox("Select Y column (y-axis)", df_line.columns)
      color_column = st.selectbox("Select color column", df_line.columns)
    
    if x_column is not None and y_column is not None:
      fig = px.scatter(df_line, x=x_column, y=y_column,height=500,color=color_column,color_discrete_sequence=['blue'],template='plotly_dark',title='Time Series Plotting')
      st.plotly_chart(fig,theme=None,use_container_width=True)
  else:
    if uploaded_file and plotting_options == 'scatter_plot':
      saved_file = st.session_state[f'{uploaded_file.name}']
      if uploaded_file.name.endswith('.txt'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter='\t')
        st.write(df_line.head())
        x_column = st.selectbox('select X column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        color_column = st.selectbox("Select color column", df_line.columns)
        
      elif uploaded_file.name.endswith('.csv'):
        df_line = pd.read_csv(StringIO(saved_file.decode('UTF-8')), skiprows=skiplines, delimiter=',')
        st.write(df_line.head())
        x_column = st.selectbox('select X column (x-axis)',df_line.columns)
        y_column = st.selectbox("Select Column to Plot (y-axis)", df_line.columns)
        color_column = st.selectbox("Select color column", df_line.columns)
        
      if x_column is not None and y_column is not None:
        fig = px.scatter(df_line, x=x_column, y=y_column,color=color_column,height=500, template='ggplot2',title='Scatter Plotting')
        st.plotly_chart(fig,theme=None,use_container_width=True)


if plotting_options == 'time_series':
  plot_time_series()
elif plotting_options == 'line_plot':
  line_plot_options()
elif plotting_options == 'bar_plot':
  bar_plot_options()
elif plotting_options == 'scatter_plot':
  scatter_plot_options()

    
