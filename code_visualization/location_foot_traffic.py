from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

def data_load(db, table):
    user_id = 'user_id'
    user_pw = 'user_pw'
    ip = 'ip'
    port = 'port'
    
    db_connection_path = f'mysql+mysqldb://{user_id}:{user_pw}@{ip}:{port}/{db}'
    
    df = pd.read_sql_table(table, con=create_engine(db_connection_path, encoding='utf-8').connect())
    return df

df_loc = data_load('team03_erd', 'Location')

seoul_geo = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'

fig = px.choropleth(df_loc, geojson=seoul_geo, locations='GU_NAME', featureidkey='properties.name',
                    color='FOOT_TRAFFIC', color_continuous_scale='Blues')
fig.update_geos(fitbounds="locations", visible=False)
fig.update_coloraxes(showscale=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, dragmode=False)

fig.show()

