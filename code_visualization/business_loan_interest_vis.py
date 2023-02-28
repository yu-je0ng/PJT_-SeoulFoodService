import plotly.express as px
import pandas as pd
import numpy as np
import pymysql

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

conn = pymysql.connect(host='35.79.131.28', user='root', password='1234', db='team03', charset='utf8')

cursor = conn.cursor()
sql = "select * from business_loan_interest;"

cursor.execute(sql)
conn.close()
result = cursor.fetchall()

test = pd.DataFrame(result)

test.columns = ['Bank', '2017', '2018', '2019']
data_to_insert = {'Bank' : 'years', '2017' : '2017', '2018' : '2018', '2019' : '2019'}
test = test.append(data_to_insert, ignore_index=True)
print(test)
test.T

temp = test.T
#temp.columns = ['BNK경남은행', 'BNK부산은행', 'DGB대구은행', 'IBK기업은행', 'KB국민은행', 'KDB산업은행', 'NH농협은행', 'SH수협은행', '광주은행', '스탠다드차타드은행', '신한은행', '우리은행', '전북은행', '제주은행', '하나은행', '한국씨티은행', 'years']
temp = temp.drop('Bank')

print(temp)
fig = px.line(temp, x=16, y=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
fig.show()



#fig = px.line(test, x='Bank', y=['2017', '2018', '2019'])

#fig.show()