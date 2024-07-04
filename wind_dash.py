import streamlit as st
import pandas as pd
import numpy as np
import os
import mplstereonet
from plots import *
from utils import *

#Strealit layout config
st.set_page_config(layout='wide')

root = "Codes//WindSpreedsheats//Aggregate"
files = os.listdir(root)
files = [f for f in files if f.split('.')[-1] == 'csv']

# Concatenate df from different years
df = pd.read_csv(os.path.join(root, files[0]))
for f in files[1:]:
     sample = pd.read_csv(os.path.join(root, f))
     df = pd.concat([df,sample])
df.reset_index(inplace=True, drop=True)


#Drop unavailable data
# Select rows where 'date' is less than the threshold
df = df[df['LOCAL_DATE'] < '2024-06-20']
df['SEASON'] = df['LOCAL_MONTH'].apply(get_season)

#Drop Nan - Here dropping columns with less than 200 instances per year
#this drop might need adjustment
null_counts = df.isnull().sum()
keep_cols = null_counts[null_counts <len(np.unique(df['LOCAL_YEAR'])) * 200].keys()
df = df.loc[:,keep_cols]




# "with" notation - select years
with st.sidebar:
    #stations = st.text_input('Select station', value='any')
    option = st.selectbox(
    "Select a station",
    ("All", "MATAGAMI", "VAL D'OR A"))

if option != 'All':
    df = df.query('STATION_NAME == @option')

with st.sidebar:
    year_min = st.number_input('Select year minimum',min_value=df['LOCAL_YEAR'].min(), max_value=df['LOCAL_YEAR'].max(),value =df['LOCAL_YEAR'].min())
    year_max = st.number_input('Select year Maximum',min_value=df['LOCAL_YEAR'].min(), max_value=df['LOCAL_YEAR'].max(), value =df['LOCAL_YEAR'].max())
    
df = df.query('LOCAL_YEAR >= @year_min')
df = df.query('LOCAL_YEAR <= @year_max')

with st.sidebar:
    season = st.selectbox(
    "Select a season",
    ("All", "WINTER", "SPRING", "SUMMER","AUTUMN"))

    month = st.selectbox(
    "Select a month if no season is selected",
    ("All", 1,2,3,4,5,6,7,8,9,10,11,12))

    if month != 'All' and season =="All":
        st.write("The current selection is the month", month)
    if season != 'All':
        st.write("The current selection is the season:", season)

    pair = st.selectbox(
    "Wish to see a pairplot?", ('NO','YES'))
    

if month != 'All' and season =="All":
    df = df.query('LOCAL_MONTH == @month')

if season != 'All':
    df = df.query('SEASON == @season')

df
# WIND Analysis
wind_direction = df['DIRECTION_MAX_GUST'] * 10
wind_speed = df['SPEED_MAX_GUST']

wind_direction = wind_direction[wind_direction>0]
wind_speed = wind_speed[wind_speed>0]

#Get graphs
wind_rose = wind_rose_diagram(wind_direction,web=True)
wind_contour = wind_speed_density(wind_direction,wind_speed,web=True)
histograms = plot_wind_hist(wind_direction, wind_speed,web=True)
hu = plot_humidity(df,web=True)
temp = plot_temperature(df,web=True)
prec = plot_precipitation(df,col='TOTAL_PRECIPITATION',web=True)


#PLot graphs
col1, col2 = st.columns(2)
st.info('The direction (true or geographic, not magnetic) from which the wind blows. '
        'It represents the average direction during the two minute period ending at the time of observation.' 
        'Expressed in tens of degrees (10s deg), 9 means 90 degrees true or an east wind, and 36 means 360 degrees true' 
    'or a wind blowing from the geographic North Pole. A value of zero (0) denotes a calm wind', icon="ℹ️")

st.info('The speed of motion of air in kilometres per hour (km/h) usually observed at 10 metres above the ground. '
        'It represents the average speed during the one-, two- or ten-minute period ending at the time of observation. ', icon='ℹ️')
col1.pyplot(wind_rose,use_container_width=True)
col2.pyplot(wind_contour,use_container_width=True)

st.plotly_chart(histograms,use_container_width=True)

#PLot graphs
st.plotly_chart(temp,use_container_width=True)

st.info('The minimum percentage (%) value of all hourly relative '
'humidity values observed at a specified location for a specified time interval.', icon='ℹ️')

st.plotly_chart(hu,use_container_width=True)


st.plotly_chart(prec,use_container_width=True)

selection = ['DIRECTION_MAX_GUST','SPEED_MAX_GUST','MEAN_TEMPERATURE','MIN_TEMPERATURE', 'MAX_TEMPERATURE','TOTAL_PRECIPITATION','MIN_REL_HUMIDITY', 'MAX_REL_HUMIDITY','SEASON']
df_aux = df.loc[:,selection]
df_aux['DIRECTION_MAX_GUST'] =df_aux['DIRECTION_MAX_GUST']*10
if pair =='YES':
    
    pairplot = get_pairplot(df_aux, columns=selection)
    st.pyplot(pairplot,use_container_width=True)


df_aux = df_aux.describe()
st.write(df_aux)

