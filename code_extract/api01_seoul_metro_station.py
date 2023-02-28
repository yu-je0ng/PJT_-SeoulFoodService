import requests
import json
import pandas as pd
import numpy as np

def api_seoul_metr():

    key = "hUjocrzIzyY2OTHu%2B1Y3%2B2fiZN5UiqpxVVqJTHuKN6MWABYTvt7mPdUaE5Ai8tY5%2F3ykm2FU22a07R%2ByeEM%2FGg%3D%3D"
    line1_resp = requests.get(f"https://api.odcloud.kr/api/15041300/v1/uddi:90c8cf16-7bc9-42a4-a219-9a54f47768ed?page=1&perPage=97&serviceKey={key}")
    line2_resp = requests.get(f"https://api.odcloud.kr/api/15041301/v1/uddi:3ecd8bc2-34ea-4860-a788-bf2578754ad9?page=1&perPage=50&serviceKey={key}")
    line3_resp = requests.get(f"https://api.odcloud.kr/api/15041302/v1/uddi:e654fca8-d6d5-4977-bf0d-a4ebea52d5b6?page=1&perPage=41&serviceKey={key}")
    line4_resp = requests.get(f"https://api.odcloud.kr/api/15041303/v1/uddi:c49053c3-6900-46c9-9615-cf5cc51c0dcc?page=1&perPage=47&serviceKey={key}")
    line5_resp = requests.get(f"https://api.odcloud.kr/api/15041304/v1/uddi:8717c1fd-0d93-465e-93fb-f34dda9612d5?page=1&perPage=51&serviceKey={key}")
    line6_resp = requests.get(f"https://api.odcloud.kr/api/15041305/v1/uddi:e405b333-40e8-44f3-b918-d0fd7e7dd7b4?page=1&perPage=34&serviceKey={key}")
    line7_resp = requests.get(f"https://api.odcloud.kr/api/15041306/v1/uddi:25014d49-e302-4157-a95d-b09a383a4774?page=1&perPage=49&serviceKey={key}")
    line8_resp = requests.get(f"https://api.odcloud.kr/api/15041334/v1/uddi:d7bacdad-8a49-4d47-8d96-b3a226db4efc?page=1&perPage=34&serviceKey={key}")
    line9_resp = requests.get(f"https://api.odcloud.kr/api/15041335/v1/uddi:515ee279-c88f-47cc-9f94-a4dac970894c?page=1&perPage=34&serviceKey={key}")


    station_list = list()
    station_list.extend(json.loads(line1_resp.text)['data_raw'])
    station_list.extend(json.loads(line2_resp.text)['data_raw'])
    station_list.extend(json.loads(line3_resp.text)['data_raw'])
    station_list.extend(json.loads(line4_resp.text)['data_raw'])
    station_list.extend(json.loads(line5_resp.text)['data_raw'])
    station_list.extend(json.loads(line6_resp.text)['data_raw'])
    station_list.extend(json.loads(line7_resp.text)['data_raw'])
    station_list.extend(json.loads(line8_resp.text)['data_raw'])
    station_list.extend(json.loads(line9_resp.text)['data_raw'])


    df_stations = pd.DataFrame(station_list)
    df_stations.to_csv('../data_raw/seoul_metro_station_api_raw.csv', encoding='utf-8', index=False)

    df_stations.drop('철도운영기관명', inplace=True, axis=1)
    df_stations = df_stations[['선명', '역명', '경도', '위도']]
    df_stations.replace('', np.nan, inplace=True)
    df_stations.dropna(axis=0, inplace=True)
    df_stations.rename(columns={'선명': 'line', '역명': 'station_name', '경도': 'longitude', '위도': 'latitude' }, inplace=True)
    df_stations.set_index('station_name', inplace=True)

    print(df_stations)
    df_stations.to_csv('../data_raw/seoul_metro_station_api_processed.csv', encoding='utf-8', index=True)