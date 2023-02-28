import plotly.express as px
import pandas as pd
import numpy as np
import pymysql

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

conn = pymysql.connect(host='35.79.131.28', user='root', password='1234', db='team03', charset='utf8')

cursor = conn.cursor()
sql = "select signguNm, count(_c0) from seoul_store_data_pre_proc group by signguNm;"

#sql = "select count(*) from seoul_store_data_pre_proc"

cursor.execute(sql)
conn.close()
result = cursor.fetchall()

test = pd.DataFrame(result)

fig = px.bar(test, x =0, y =1)

fig.show()



