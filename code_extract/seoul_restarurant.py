import pandas as pd
import requests

import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint

def crawl_seoul_restaurant():

    key = "key"
    d_type = 'xml'
    start_page = '1'
    end_page = '1000'

    url = 'http://openapi.seoul.go.kr:8088/'+ key +'/'+ d_type +'/LOCALDATA_072404/'+ start_page +'/'+ end_page + '/'

    df = pd.read_xml(url)

    x = 1001

    for i in range(2000, 500000, 1000):
        try:
            url = 'http://openapi.seoul.go.kr:8088/' + key + '/' + d_type + '/LOCALDATA_072404/' + str(x) + '/' + str(
                i) + '/'

            x = x + 1000

            df2 = pd.read_xml(url)

            df = pd.concat([df, df2])


        except:
            pass

    df

    df.drop([0, 1], axis=0, inplace=True)

    data = df[['BPLCNM','TRDSTATENM', 'SITEPOSTNO', 'SITEWHLADDR', 'RDNWHLADDR', 'X', 'Y']]

    data.reset_index(inplace=True, drop=True)

    data['TRDSTATENM'].unique()

    #fig = plt.figure()

    #sns.countplot(data= data, x='TRDSTATENM')

    #plt.show()

    close_idx = data[data['TRDSTATENM'].str.contains("폐업")].index

    data.drop(close_idx, inplace=True)

    data.reset_index(inplace=True, drop=True)
    data

    data.to_csv('C:/worksplaces/workspace_project/project_visual/restaurant_data/data/restaurant.csv', encoding='utf-8', index=True)
