import plotly.express as px
import pandas as pd
import numpy as np
import pymysql

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

conn = pymysql.connect(host='host', user='user', password='password', db='team03', charset='utf8')

cursor = conn.cursor()
sql = "select * from consumer_price_index;"

cursor.execute(sql)
conn.close()
result = cursor.fetchall()

test = pd.DataFrame(result)

test.columns = ['years', 'CPI', 'CPI_inflation']

fig = px.line(test, x='years', y='CPI_inflation')
fig.show()
